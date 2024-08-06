import csv
import os
import re
import requests
from collections import OrderedDict
from typing import List, Tuple

# Functions to compute fields for simulations ###########################################
def get_data_size_and_hpss(hpss_path: str) -> Tuple[str, str]:
        """Get the data size in TB"""
        output = "out.txt"
        if os.path.exists(output):
            os.remove(output)
        os.system(f'(hsi "du {hpss_path}") 2>&1 | tee {output}')
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
            hpss = hpss_path
        else:
            data_size = ""
            hpss = ""
        return (data_size, hpss)

def get_esgf(source_id: str, model_version: str, experiment: str, ensemble_num: str, link_type: str) -> str:
    if experiment and ensemble_num:
        # See https://github.com/E3SM-Project/CMIP6-Metadata/pull/9#issuecomment-1246086256 for the table of ensemble numbers
        # Note that `[1:]`` removes `v` from `model_version`
        # 
        # Query parameters:
        # v2:
        # Native (model_version, experiment, ensemble_member)
        # CMIP6 (source_id, experiment_id, variant_label)
        # v1 on https://e3sm.org/data/get-e3sm-data/released-e3sm-data/v1-1-deg-data-cmip6/:
        # Native (experiment, and optionally model_version)
        # CMIP6 (activity_id, source_id, experiment_id)

        # TODO: figure out if we're returning the correct things
        # Comparison to links on https://portal.nersc.gov/project/e3sm/forsyth/data_docs/html/v1/WaterCycle/simulation_data/simulation_table.html
        # simulation | e3sm.org CMIP6 | e3sm.org Native | data_docs CMIP6 | data_docs Native |
        # piControl              | 346   | 67 | 346  | 15 |
        # historical             | 3414 | 190 | 1420 | 70 | 5 rows on data_docs
        # 1pctCO2                | 339  | 38  | 339  | 14 |
        # abrupt-4xCO2           | 293  | 50  | 0    | 14 | 2 rows on data_docs
        # abrupt-4xCO2-ext300yrs | x    | 14  |
        # amip                   | 527  | 30  | 527  | 30 | 3 rows on data_docs
        # amip_1850_allF         | x    | 30  |
        # amip_1850_aeroF        | x    | 30  |
        # TODO: only return Native for some experiments...
        esgf_native = f"`Native <https://esgf-node.llnl.gov/search/e3sm/?model_version={model_version[1:]}_0&experiment={experiment}&ensemble_member=ens{ensemble_num}>`_"
        if experiment == 'hist-all-xGHG-xaer':
            experiment_id = 'hist-nat'
        else:
            experiment_id = experiment
        esgf_cmip = f"`CMIP <https://esgf-node.llnl.gov/search/cmip6/?source_id={source_id}&experiment_id={experiment_id}&variant_label=r{ensemble_num}i1p1f1>`_"
        if link_type == "cmip":
            esgf = esgf_cmip
        elif link_type == "native":
            esgf = esgf_native
        else:
            esgf = esgf_cmip + ', ' + esgf_native
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

# Define simulations and their grouping ###########################################
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
            hpss_path = simulation_dict["hpss_path"]
        else:
            hpss_path = f"/home/projects/e3sm/www/{self.group}/E3SM{self.model_version}/{self.resolution}/{self.simulation_name}"
        self.data_size, self.hpss = get_data_size_and_hpss(hpss_path)

        if self.resolution == "NARRM":
            source_id = f"E3SM-{self.model_version[1:]}-0-{self.resolution}"
        else:
            source_id = f"E3SM-{self.model_version[1:]}-0"
        self.esgf = get_esgf(source_id, self.model_version, self.experiment, self.ensemble_num, self.link_type)

        self.run_script_original = get_run_script_original(self.model_version, self.simulation_name)
        self.run_script_reproduction = get_run_script_reproduction(self.model_version, self.simulation_name)

    def get_row(self, output_file):
        if output_file.endswith("simulation_table.rst"):
            return [self.simulation_name, self.data_size, self.esgf, self.hpss]
        elif output_file.endswith("reproduction_table.rst"):
            return [self.simulation_name, self.machine, self.run_script_reproduction, self.checksum]
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

# Construct simulations ###########################################
def parse_hpss_path(simulation_dictionary):
    hpss_path = simulation_dictionary["hpss_path"]
    model_version = simulation_dictionary["model_version"]
    group = simulation_dictionary["group"]
    subdir = os.path.basename(hpss_path)
    simulation_dictionary["simulation_name"] = subdir
    if (model_version == "v1" ) and (group == "WaterCycle"):
        # Example: 20191019.DECKv1b_P3_SSP5-8.5-GHG.ne30_oEC.cori-knl
        match_object = re.search("[0-9]{8}\.([^_]*)_(.*)\..*\.(.*)", subdir)
        if match_object:
            category = match_object.group(1)
            experiment = match_object.group(2)
            machine = match_object.group(3)
            if category.endswith("v1b"):
                # Remove "v1b"
                category = category[:-3]
            if subdir == "20190722.DECKv1b_abrupt4xCO2.ne30_oEC3.compy":
                experiment = "abrupt-4xCO2-ext300yrs"
            if experiment.startswith("H"):
                if experiment.endswith("hist-GHG"):
                    experiment = "damip_historical_hist_GHG"
                else:
                    experiment = "historical"
            elif experiment.startswith("A"):
                if experiment.endswith("allF"):
                    experiment = "amip_1850_allF"
                elif experiment.endswith("aeroF"):
                    experiment = "amip_1850_aeroF"
                else:
                    experiment = "amip"
            elif experiment.startswith("P"):
                if experiment.endswith("GHG"):
                    experiment = "damip_ssp5_8_5_ghg"
                else:
                    experiment = "projection"
            simulation_dictionary["category"] = category
            simulation_dictionary["experiment"] = experiment
            simulation_dictionary["machine"] = machine

def read_simulations(csv_file):
    # model_version > group > resolution > category > simulation_name, 
    versions: OrderedDict[str: ModelVersion] = OrderedDict()
    with open(csv_file, newline='') as opened_file:
        reader = csv.reader(opened_file)
        header: List[str] = []
        for row in reader:
            # Get labels
            if header == []:
                for label in row:
                    header.append(label.strip())
            else: 
                simulation_dict = {}
                for i in range(len(header)):
                    label = header[i]
                    simulation_dict[label] = row[i].strip()
                if "hpss_path" in simulation_dict:
                    parse_hpss_path(simulation_dict)
                if "cmip_only" in simulation_dict:
                    simulation_dict["link_type"] = "cmip"
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

# Construct table display of simulations ###########################################
def pad_cells(cells, col_divider, cell_paddings):
    string = col_divider
    for i in range(len(cells)):
        string += " " + cells[i].ljust(cell_paddings[i] + 1) + col_divider
    string += "\n"
    return string

def pad_cells_row_dividers(marker, cell_paddings):
    string = "+"
    for i in range(len(cell_paddings)):
        string += marker*(cell_paddings[i]+2) + "+"
    string += "\n"
    return string
                    
def generate_table(page_type: str, resolutions: OrderedDict[str, Category], header_cells: List[str], output_file: str, cell_paddings: List[int]):
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

def construct_pages(csv_file, model_version, group_name):
    versions: OrderedDict[str, ModelVersion] = read_simulations(csv_file)
    resolutions: OrderedDict[str, Category] = versions[model_version].groups[group_name].resolutions
    generate_table(
        f"{model_version} {group_name} simulation table",
        resolutions,
        ["Simulation", "Data Size (TB)", "ESGF Links", "HPSS Path"],
        f"../docs/source/{model_version}/{group_name}/simulation_data/simulation_table.rst",
        [65, 15, 400, 90]
    )
    generate_table(
        f"{model_version} {group_name} reproduction table",
        resolutions,
        ["Simulation", "Machine", "Script", "10 day checksum"],
        f"../docs/source/{model_version}/{group_name}/reproducing_simulations/reproduction_table.rst",
        [65, 11, 200, 34]
    )
                    
if __name__ == "__main__":
    #construct_pages("simulations.csv", "v2", "WaterCycle")
    construct_pages("simulations_v1_water_cycle.csv", "v1", "WaterCycle")