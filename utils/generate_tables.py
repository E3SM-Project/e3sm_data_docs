import csv
import os
import re
import requests
from collections import OrderedDict
from typing import Dict, List, Tuple
import urllib.parse

# Functions to compute fields for simulations #################################
def get_data_size_and_hpss(hpss_path: str) -> Tuple[str, str]:
        """Get the data size in TB"""
        is_symlink: bool = check_if_symlink(hpss_path)
        output = "out_du.txt"
        if os.path.exists(output):
            os.remove(output)
        try:
            if is_symlink:
                # The `/*` expands symlinks on HSI!
                # This will actually work fine even if it's not a symlink,
                # but we needed to check for symlinks anyway to note "(symlink)" by the HPSS path,
                # so we might as well handle the cases separately here.
                os.system(f'(hsi "du {hpss_path}/*") 2>&1 | tee {output}')
            else:
                os.system(f'(hsi "du {hpss_path}") 2>&1 | tee {output}')
        except Exception as e:
            print(f"hsi failed: {e}")
            return ("", "")
        num_bytes = "0"
        with open(output, "r") as f:
            for line in f:
                match_object = re.search("No such file or directory", line)
                if match_object:
                    break
                match_object = re.search("\((.*) bytes\)", line)
                if match_object:
                    num_bytes = match_object.group(1).replace(",", "")
                    break

        # Convert to TB
        data_size = int(num_bytes)/1e12
        if data_size > 0:
            data_size = f"{data_size:.0f}"
            if is_symlink:
                hpss = f"(symlink) {hpss_path}"
            else:
                hpss = hpss_path
        else:
            data_size = ""
            hpss = ""
        return (data_size, hpss)

def check_if_symlink(hpss_path: str) -> bool:
    output: str = "out_symlink_check.txt"
    if os.path.exists(output):
        os.remove(output)
    try:
        os.system(f'(hsi "ls {hpss_path}") 2>&1 | tee {output}')
    except Exception as e:
        print(f"hsi failed: {e}")
        return False
    with open(output, "r") as f:
        for line in f:
            # Symlinks on HSI/HPSS end in `@`
            match_object = re.search(f"{os.path.basename(hpss_path)}@", line)
            if match_object:
                return True
    return False


def get_esgf(model_version: str, resolution: str, simulation_name: str, experiment: str, ensemble_num: str, link_type: str, node: str) -> str:
    esgf: str
    if link_type == "none":
        esgf = ""
    elif model_version == "v1":
        v1_institution_id: str
        variant_suffix: str
        if simulation_name.startswith("LE_"):
            v1_institution_id = "UCSB"
            variant_suffix = "i2p2f1"
        else:
            v1_institution_id = "E3SM-Project"
            variant_suffix = "i1p1f1"
        human_readable_active_facets: str = f'{{"institution_id":"{v1_institution_id}","source_id":"E3SM-1-0","experiment_id":"{experiment}","variant_label":"r{ensemble_num}{variant_suffix}"}}'
        url_active_facets: str = urllib.parse.quote(human_readable_active_facets)
        esgf = f"`CMIP <https://esgf-node.{node}.gov/search?project=CMIP6&activeFacets={url_active_facets}>`_"
    else:
        # v2, v2.1
        # Determine source_id
        if (len(model_version) == 4) and (model_version[2] == "."):
            source_id = f"E3SM-{model_version[1]}-{model_version[3]}"
        elif (len (model_version) == 2):
            if resolution == "NARRM":
                source_id = f"E3SM-{model_version[1]}-0-{resolution}"
            else:
                source_id = f"E3SM-{model_version[1]}-0"
        else:
            raise RuntimeError(f"Invalid model-version={model_version}")
        # Determine esgf
        if node == "cels.anl": # v2.1 only
            human_readable_active_facets = f'{{"source_id":"{source_id}","experiment_id":"{experiment}","variant_label":"r{ensemble_num}i1p1f1"}}'
            url_active_facets: str = urllib.parse.quote(human_readable_active_facets)
            esgf = f"`CMIP <https://esgf-node.{node}.gov/search/?project=CMIP6&activeFacets={url_active_facets}>`_"
        elif experiment and ensemble_num:
            # See https://github.com/E3SM-Project/CMIP6-Metadata/pull/9#issuecomment-1246086256 for the table of ensemble numbers
            # Note that `[1:]`` removes `v` from `model_version`
            esgf_native: str = f"`Native <https://esgf-node.{node}.gov/search/e3sm/?model_version={model_version[1:]}_0&experiment={experiment}&ensemble_member=ens{ensemble_num}>`_"
            if experiment == 'hist-all-xGHG-xaer':
                experiment_id = 'hist-nat'
            else:
                experiment_id = experiment
            esgf_cmip: str = f"`CMIP <https://esgf-node.{node}.gov/search/cmip6/?source_id={source_id}&experiment_id={experiment_id}&variant_label=r{ensemble_num}i1p1f1>`_"
            if link_type == "cmip":
                esgf = esgf_cmip
            elif link_type == "native":
                esgf = esgf_native
            elif link_type == "both":
                esgf = esgf_cmip + ', ' + esgf_native
            else:
                raise ValueError(f"Invalid link_type={link_type}")
        else:
            esgf = ""
    return esgf

def get_run_script_original(model_version: str, simulation_name: str) -> str:
    run_script_original = f"https://github.com/E3SM-Project/e3sm_data_docs/tree/main/run_scripts/{model_version}/original/run.{simulation_name}.sh"
    response = requests.get(run_script_original).status_code
    if response == 200:
        run_script_original = f"`{simulation_name} <{run_script_original}>`_"
    else:
        run_script_original = ""
    return run_script_original

def get_run_script_reproduction(model_version: str, simulation_name: str) -> str:
    run_script_reproduction = f"https://raw.githubusercontent.com/E3SM-Project/e3sm_data_docs/main/run_scripts/{model_version}/reproduce/run.{simulation_name}.sh"
    response = requests.get(run_script_reproduction).status_code
    if response == 200:
        run_script_reproduction = f"`{simulation_name} <{run_script_reproduction}>`_"
    else:
        run_script_reproduction = ""
    return run_script_reproduction

# Define simulations and their grouping #######################################
class Simulation(object):
    def __init__(self, simulation_dict):
        self.model_version = simulation_dict["model_version"]
        self.group = simulation_dict["group"]
        self.resolution = simulation_dict["resolution"]
        #self.category = simulation_dict["category"]
        self.simulation_name = simulation_dict["simulation_name"]
        self.machine = simulation_dict["machine"]
        self.checksum = simulation_dict["checksum"]
        self.experiment = simulation_dict["experiment"]

        self.ensemble_num = simulation_dict["ensemble_num"]
        self.link_type = simulation_dict["link_type"]

        if "hpss_path" in simulation_dict:
            # If `hpss_path` is specified, then it's a non-standard path
            hpss_path = simulation_dict["hpss_path"]
        else:
            hpss_path = f"/home/projects/e3sm/www/{self.group}/E3SM{self.model_version}/{self.resolution}/{self.simulation_name}"
        if "node" in simulation_dict.keys():
            self.node = simulation_dict["node"]
        else:
            self.node = "llnl"

        if "." in self.model_version:
            displayed_version: str = self.model_version.replace(".", "_")
            hpss_path = f"/home/projects/e3sm/www/{self.group}/E3SM{displayed_version}/{self.simulation_name}"
        else:
            hpss_path = f"/home/projects/e3sm/www/{self.group}/E3SM{self.model_version}/{self.resolution}/{self.simulation_name}"
        self.data_size, self.hpss = get_data_size_and_hpss(hpss_path)

        self.esgf = get_esgf(self.model_version, self.resolution, self.simulation_name, self.experiment, self.ensemble_num, self.link_type, self.node)

        # Generate web interface URL from HPSS path
        self.web_interface = self.get_web_interface_url()

        self.run_script_original = get_run_script_original(self.model_version, self.simulation_name)
        self.run_script_reproduction = get_run_script_reproduction(self.model_version, self.simulation_name)
        
        if not self.checksum:
            self.checksum = "N/A"
        if not self.run_script_reproduction:
            self.run_script_reproduction = "N/A"
        if not self.run_script_original:
            self.run_script_original = "N/A"

    def get_web_interface_url(self) -> str:
        """Generate web interface URL from HPSS path"""
        if self.hpss and self.data_size:
            # Convert HPSS path to web interface URL
            # /home/projects/e3sm/www/CoupledSystem/E3SMv3/LR/v3.LR.piControl -> https://portal.nersc.gov/archive/home/projects/e3sm/www/CoupledSystem/E3SMv3/LR/v3.LR.piControl
            hpss_clean = self.hpss.replace("(symlink) ", "")  # Remove symlink prefix if present
            # Use the full path - each simulation gets its own distinct URL
            web_url = f"https://portal.nersc.gov/archive{hpss_clean}"
            return f"`HPSS URL <{web_url}>`_"
        return ""

    def get_row(self, output_file, minimal_content: bool = False) -> List[str]:
        if "simulation" in output_file:
            row = [self.simulation_name, self.data_size, self.esgf, self.hpss, self.web_interface]
            if minimal_content:
                match_object: re.Match = re.match("`.*<(.*)>`_", self.esgf)
                if match_object:
                    row[2] = match_object.group(1)  # Extract URL from the esgf link
                if self.hpss.startswith("(symlink) "):
                    # Remove symlink prefix for the HPSS path
                    # Since we don't want that in the csv output,
                    # which a computer reads.
                    row[3] = row[3].replace("(symlink) ", "")
                # Extract web interface URL for CSV
                web_match: re.Match = re.match("`.*<(.*)>`_", self.web_interface)
                if web_match:
                    row[4] = web_match.group(1)  # Extract URL from the web interface link
            return row
        elif "reproduction" in output_file:
            return [self.simulation_name, self.machine, self.checksum, self.run_script_reproduction, self.run_script_original]
        else:
            raise RuntimeError(f"Invalid output_file={output_file}")

class Category(object):
    def __init__(self, name):
        self.name = name
        self.simulations: OrderedDict[Simulation] = OrderedDict()

    def append(self, simulation):
        self.simulations.update([(simulation.simulation_name, simulation)])

class Resolution(object):
    def __init__(self, name):
        self.name = name
        self.categories: OrderedDict[Category] = OrderedDict()

    def append(self, category):
        self.categories.update([(category.name, category)])

class Group(object):
    def __init__(self, name):
        self.name = name
        self.resolutions: OrderedDict[Resolution] = OrderedDict()

    def append(self, resolution):
        self.resolutions.update([(resolution.name, resolution)])

class ModelVersion(object):
    def __init__(self, name):
        self.name = name
        self.groups: OrderedDict[Group] = OrderedDict()

    def append(self, group):
        self.groups.update([(group.name, group)])

# Construct simulations #######################################################

def read_simulations(csv_file):
    # model_version > group > resolution > category > simulation_name, 
    versions: OrderedDict[str: ModelVersion] = OrderedDict()
    with open(csv_file, newline='') as opened_file:
        reader = csv.reader(opened_file)
        header: List[str] = []
        simulation_dicts: List[Dict[str, str]] = []
        # First, just set up the dictionary, to make sure all the necessary data is available.
        for row in reader:
            # Get labels
            if header == []:
                for label in row:
                    header.append(label.strip())
            else: 
                simulation_dict = {}
                for i in range(len(header)):
                    label = header[i]
                    if len(row) != len(header):
                        raise RuntimeError(f"header has {len(header)} labels, but row={row} has {len(row)} entries")
                    simulation_dict[label] = row[i].strip()
                if "cmip_only" in simulation_dict.keys():
                    # Backwards compatibility for v2, v2.1 csv files
                    if simulation_dict["cmip_only"] == "":
                        simulation_dict["link_type"] = "both"
                    elif simulation_dict["cmip_only"] == "cmip_only":
                        simulation_dict["link_type"] = "cmip"
                    else:
                        raise ValueError(f"Invalid cmip_only={simulation_dict['cmip_only']}")
                simulation_dicts.append(simulation_dict)
        # Now, that we have valid dictionaries for each simulation, let's construct objects
        for simulation_dict in simulation_dicts:
            model_version_name = simulation_dict["model_version"]
            group_name = simulation_dict["group"]
            resolution_name = simulation_dict["resolution"]
            category_name = simulation_dict["category"]
            if model_version_name not in versions:
                v = ModelVersion(model_version_name)
                versions.update([(model_version_name, v)])
            else:
                v = versions[model_version_name]
            if group_name not in v.groups:
                g = Group(group_name)
                v.groups.update([(group_name, g)])
            else:
                g = v.groups[group_name]
            if resolution_name not in g.resolutions:
                r = Resolution(resolution_name)
                g.resolutions.update([(resolution_name, r)])
            else:
                r = g.resolutions[resolution_name]
            if category_name not in r.categories:
                c = Category(category_name)
                r.categories.update([(category_name, c)])
            else:
                c = r.categories[category_name]
            s = Simulation(simulation_dict)
            c.simulations.update([(s.simulation_name, s)])
    return versions

# Construct output csv ########################################################

def construct_output_csv(resolutions: OrderedDict[str, Category], header_cells: List[str], output_file: str):
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header_cells)
        for resolution in resolutions.values():
            for category in resolution.categories.values():
                for simulation in category.simulations.values():
                    writer.writerow(simulation.get_row(output_file, minimal_content=True))

# Construct table display of simulations ######################################
def pad_cells(cells: List[str], col_divider: str, cell_paddings: List[int]) -> str:
    string = col_divider
    for i in range(len(cells)):
        if len(cells[i]) > cell_paddings[i]:
            s = f"WARNING: cell padding={cell_paddings[i]} is insufficient for {cells[i]} of length {len(cells[i])}"
            raise RuntimeError(s)
        string += " " + cells[i].ljust(cell_paddings[i] + 1) + col_divider
    string += "\n"
    return string

def pad_cells_row_dividers(marker: str, cell_paddings: List[int]) -> str:
    string = "+"
    for i in range(len(cell_paddings)):
        string += marker*(cell_paddings[i]+2) + "+"
    string += "\n"
    return string
                    
def generate_table(page_type: str, resolutions: OrderedDict[str, Category], header_cells: List[str], output_file: str, cell_paddings: List[int]):

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w") as file_write:
        # Page Title
        file_write.write("**********************************\n")
        file_write.write(f"{page_type}\n")
        file_write.write("**********************************\n\n")
        # Table Header
        file_write.write(pad_cells_row_dividers("-", cell_paddings))
        file_write.write(pad_cells(header_cells, "|", cell_paddings))
        file_write.write(pad_cells_row_dividers("=", cell_paddings))
        # Table Body
        for resolution in resolutions.values():
            for category in resolution.categories.values():
                # Category rows
                category_cells = [""]*len(header_cells)
                category_cells[0] = f"**{resolution.name} > {category.name}**"
                file_write.write(pad_cells(category_cells, "|", cell_paddings))
                file_write.write(pad_cells_row_dividers("-", cell_paddings))
                for simulation in category.simulations.values():
                    # Simulation rows
                    file_write.write(pad_cells(simulation.get_row(output_file), "|", cell_paddings))
                    file_write.write(pad_cells_row_dividers("-", cell_paddings))

def construct_pages(csv_file: str, model_version: str, group_name: str, include_reproduction_scripts: bool = False):
    versions: OrderedDict[str, ModelVersion] = read_simulations(csv_file)
    resolutions: OrderedDict[str, Category] = versions[model_version].groups[group_name].resolutions
    header_cells: List[str] = ["Simulation", "Data Size (TB)", "ESGF Links", "HPSS Path", "HPSS URL"]
    construct_output_csv(resolutions, header_cells, f"../machine_readable_data/{model_version}_{group_name}_simulations.csv")
    print(f"csv of the simulations will be available at https://github.com/E3SM-Project/e3sm_data_docs/blob/main/machine_readable_data/{model_version}_{group_name}_simulations.csv")
    # TODO: add proper subdirs and index.rst files in docs/
    generate_table(
        f"{model_version} {group_name} simulation table",
        resolutions,
        header_cells,
        f"../docs/source/{model_version}/{group_name}/simulation_data/simulation_table.rst",
        [65, 15, 220, 120, 140]
    )
    if include_reproduction_scripts:
        header_cells_reproduction: List[str] = ["Simulation", "Machine", "10 day checksum", "Reproduction Script", "Original Script (requires significant changes to run!!)",]
        construct_output_csv(resolutions, header_cells_reproduction, f"../machine_readable_data/{model_version}_{group_name}_reproductions.csv")
        print(f"csv of the reproductions will be available at https://github.com/E3SM-Project/e3sm_data_docs/blob/main/machine_readable_data/{model_version}_{group_name}_reproductions.csv")
        generate_table(
            f"{model_version} {group_name} reproduction table",
            resolutions,
            header_cells_reproduction,
            f"../docs/source/{model_version}/{group_name}/reproducing_simulations/reproduction_table.rst",
            # TODO: The script boxes have to be 200 characters wide to fit in the links...
            # This is unfortunate because the actual displayed text is quite short.
            # https://github.com/E3SM-Project/e3sm_data_docs/issues/30 may fix this.
            [65, 11, 34, 200, 200]
        )
                    
if __name__ == "__main__":
    #construct_pages("simulations_v2.csv", "v2", "WaterCycle")
    #construct_pages("simulations_v2_1.csv", "v2.1", "WaterCycle")
    #construct_pages("simulations_v2_1.csv", "v2.1", "BGC")
    # 
    # Sources for v1 data
    # https://acme-climate.atlassian.net/wiki/spaces/ED/pages/4495441922/V1+Simulation+backfill+WIP
    # https://acme-climate.atlassian.net/wiki/spaces/DOC/pages/1271169273/v1+High+Res+Coupled+Run+Output+HPSS+Archive 
    # construct_pages("input/simulations_v1_water_cycle.csv", "v1", "WaterCycle")
    construct_pages("input/simulations_v3_LR_coupled.csv", "v3", "CoupledSystem")
