import csv
import os
import re
import requests

class Simulation(object):
    def __init__(self, name, resolution, experiment=None, ensemble_num=None):
        self.name = name
        
        hpss_path = f"/home/projects/e3sm/www/WaterCycle/E3SMv2/{resolution}/{name}"
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
            
        data_size = int(num_bytes)/1e12
        if data_size > 0:
            # Convert to TB
            self.data_size = f"{data_size:.0f}"
            self.hpss = hpss_path
        else:
            self.data_size = ""
            self.hpss = ""

        if experiment and ensemble_num:
            # See https://github.com/E3SM-Project/CMIP6-Metadata/pull/9#issuecomment-1246086256 for the table of ensemble numbers
            self.esgf = f"`{name} <https://esgf-node.llnl.gov/search/e3sm/?model_version=2_0&experiment={experiment}&ensemble_member=ens{ensemble_num}>`_"
        else:
            self.esgf = ""

        run_script_original = f"https://github.com/E3SM-Project/e3sm_data_docs/tree/main/run_scripts/original/run.{name}.sh"
        response = requests.get(run_script_original).status_code
        if response == 200:
            self.run_script_original = f"`{name} <{run_script_original}>`_"
        else:
            self.run_script_original = ""

        self.run_script_reproduction = "TBD"

    def get_row(self):
        return [self.name, self.data_size, self.esgf, self.hpss, self.run_script_original, self.run_script_reproduction]


class Category(object):
    def __init__(self, name):
        self.name = name
        self.simulations = []

    def append(self, simulation):
        self.simulations.append(simulation)

class Resolution(object):
    def __init__(self, name):
        self.name = name
        self.categories = []

    def append(self, category):
        self.categories.append(category)

def create_simulation_objects():
    low_res = Resolution("Water Cycle (low-resolution)")

    deck = Category("DECK")
    low_res.append(deck)
    simulation_tuples = [
        ("v2.LR.piControl","LR", "piControl", 1),
        ("v2.LR.piControl_land", "LR", None, None),
        ("v2.LR.abrupt-4xCO2_0101", "LR", "abrupt-4xCO2", 1),
        ("v2.LR.abrupt-4xCO2_0301", "LR", "abrupt-4xCO2", 2),
        ("v2.LR.1pctCO2_0101", "LR", "1pctCO2", 1),
    ]
    for simulation_tuple in simulation_tuples:
        deck.append(Simulation(*simulation_tuple))

    historical = Category("Historical")
    low_res.append(historical)
    simulation_tuples = [
        ("v2.LR.historical_0101", "LR", "historical", 1),
        ("v2.LR.historical_0151", "LR", "historical", 2),
        ("v2.LR.historical_0201", "LR", "historical", 3),
        ("v2.LR.historical_0251", "LR", "historical", 4),
        ("v2.LR.historical_0301", "LR", "historical", 5),
        ("v2.LR.historical_0101_bonus", "LR", None, None),
    ]
    for simulation_tuple in simulation_tuples:
        historical.append(Simulation(*simulation_tuple))

    historical_le = Category("Historical LE")
    low_res.append(historical_le)
    simulation_tuples = [
        ("v2.LR.historical_0111", "LR"),
        ("v2.LR.historical_0121", "LR"),
        ("v2.LR.historical_0131", "LR"),
        ("v2.LR.historical_0141", "LR"),
        ("v2.LR.historical_0161", "LR"),
        ("v2.LR.historical_0171", "LR"),
        ("v2.LR.historical_0181", "LR"),
        ("v2.LR.historical_0191", "LR"),
        ("v2.LR.historical_0211", "LR"),
        ("v2.LR.historical_0221", "LR"),
        ("v2.LR.historical_0231", "LR"),
        ("v2.LR.historical_0241", "LR"),
        ("v2.LR.historical_0261", "LR"),
        ("v2.LR.historical_0271", "LR"),
        ("v2.LR.historical_0281", "LR"),
        ("v2.LR.historical_0291", "LR"),
    ]
    for simulation_tuple in simulation_tuples:
        historical_le.append(Simulation(*simulation_tuple))

    single_forcing = Category("Single-forcing (DAMIP-like)")
    low_res.append(single_forcing)
    simulation_tuples = [
        ("v2.LR.hist-GHG_0101", "LR", "hist-GHG", 1),
        ("v2.LR.hist-GHG_0151", "LR", "hist-GHG", 2),
        ("v2.LR.hist-GHG_0201", "LR", "hist-GHG", 3),
        ("v2.LR.hist-GHG_0251", "LR", "hist-GHG", 4),
        ("v2.LR.hist-GHG_0301", "LR", "hist-GHG", 5),
        ("v2.LR.hist-aer_0101", "LR", "hist-aer", 1),
        ("v2.LR.hist-aer_0151", "LR", "hist-aer", 2),
        ("v2.LR.hist-aer_0201", "LR", "hist-aer", 3),
        ("v2.LR.hist-aer_0251", "LR", "hist-aer", 4),
        ("v2.LR.hist-aer_0301", "LR", "hist-aer", 5),
        ("v2.LR.hist-all-xGHG-xaer_0101", "LR", None, None),
        ("v2.LR.hist-all-xGHG-xaer_0151", "LR", None, None),
        ("v2.LR.hist-all-xGHG-xaer_0201", "LR", None, None),
        ("v2.LR.hist-all-xGHG-xaer_0251", "LR", None, None),
        ("v2.LR.hist-all-xGHG-xaer_0301", "LR", None, None),
    ]
    for simulation_tuple in simulation_tuples:
        single_forcing.append(Simulation(*simulation_tuple))


    amip = Category("AMIP")
    low_res.append(amip)
    simulation_tuples = [
        ("v2.LR.amip_0101", "LR", "amip", 1),
        ("v2.LR.amip_0201", "LR", "amip", 2),
        ("v2.LR.amip_0301", "LR", "amip", 3),
        ("v2.LR.amip_0101_bonus", "LR", None, None)
    ]
    for simulation_tuple in simulation_tuples:
        amip.append(Simulation(*simulation_tuple))

    rfmip = Category("RFMIP")
    low_res.append(rfmip)
    simulation_tuples = [
        ("v2.LR.piClim-control", "LR", "piClim-control", 1),
        ("v2.LR.piClim-histall_0021", "LR", "piClim-histall", 1),
        ("v2.LR.piClim-histall_0031", "LR", "piClim-histall", 2),
        ("v2.LR.piClim-histall_0041", "LR", "piClim-histall", 3),
        ("v2.LR.piClim-histaer_0021", "LR", "piClim-histaer", 1),
        ("v2.LR.piClim-histaer_0031", "LR", "piClim-histaer", 2),
        ("v2.LR.piClim-histaer_0041", "LR", "piClim-histaer", 3)
    ]
    for simulation_tuple in simulation_tuples:
        rfmip.append(Simulation(*simulation_tuple))

    other = Category("Other")
    low_res.append(other)
    simulation_tuples = [
        ("v2_ndgclim_t6h_1850aer", "LR"),
        ("v2_ndgclim_t6h_2010aer", "LR"),
    ]
    for simulation_tuple in simulation_tuples:
        other.append(Simulation(*simulation_tuple))

    rrm = Resolution("Water Cycle (NARRM)")

    deck = Category("DECK")
    rrm.append(deck)
    simulation_tuples = [
        ("v2.NARRM.piControl", "NARRM"),
        ("v2.NARRM.abrupt-4xCO2_0101", "NARRM"),
        ("v2.NARRM.1pctCO2_0101", "NARRM"),
    ]
    for simulation_tuple in simulation_tuples:
        deck.append(Simulation(*simulation_tuple))

    historical = Category("Historical")
    rrm.append(historical)
    simulation_tuples = [
        ("v2.NARRM.historical_0101", "NARRM"),
        ("v2.NARRM.historical_0151", "NARRM"),
        ("v2.NARRM.historical_0201", "NARRM"),
        ("v2.NARRM.historical_0251", "NARRM"),
        ("v2.NARRM.historical_0301", "NARRM"),
        ("v2.NARRM.historical_0101_bonus", "NARRM"),
    ]
    for simulation_tuple in simulation_tuples:
        historical.append(Simulation(*simulation_tuple))

    amip = Category("AMIP")
    rrm.append(amip)
    simulation_tuples = [
        ("v2.NARRM.amip_0101", "NARRM"),
        ("v2.NARRM.amip_0201", "NARRM"),
        ("v2.NARRM.amip_0301", "NARRM"),
        ("v2.NARRM.amip_0101_bonus", "NARRM"),
    ]
    for simulation_tuple in simulation_tuples:
        amip.append(Simulation(*simulation_tuple))

    other = Category("Other")
    rrm.append(other)
    simulation_tuples = [
        ("v2.NA.F20TR.6h.f1.1850aer", "NARRM"),
        ("v2.NA.F20TR.6h.f1.2010aer", "NARRM"),
    ]
    for simulation_tuple in simulation_tuples:
        other.append(Simulation(*simulation_tuple))
        
    return [low_res, rrm]

def get_simulation(resolution_list, simulation_name):
    for resolution in resolution_list:
        for category in resolution.categories:
            for simulation in category.simulations:
                if simulation.name == simulation_name:
                    return simulation
    return None

def pad_cells(cells, col_divider):
    string = col_divider
    string += f" {cells[0]:<65} " + col_divider
    string += f" {cells[1]:<15} " + col_divider
    string += f" {cells[2]:<150} " + col_divider
    string += f" {cells[3]:<80} " + col_divider
    string += f" {cells[4]:<200} " + col_divider
    string += f" {cells[5]:<25} " + col_divider
    string += "\n"
    return string

def pad_cells_row_dividers(marker):
    string = "+"
    string += marker*67 + "+"
    string += marker*17 + "+"
    string += marker*152 + "+"
    string += marker*82 + "+"
    string += marker*202 + "+"
    string += marker*27 + "+"
    string += "\n"
    return string

def generate_table():
    resolution_list = create_simulation_objects()
    header_cells = ["Simulation", "Data Size (TB)", "ESGF Link", "HPSS Path", "Original Run Script", "Reproduction Run Script"]
    with open("simulation_table.txt", "w") as file_write:
        file_write.write(pad_cells_row_dividers("-"))
        file_write.write(pad_cells(header_cells, "|"))
        file_write.write(pad_cells_row_dividers("="))
        for resolution in resolution_list:
            for category in resolution.categories:
                category_cells = [f"**{resolution.name} > {category.name}**", "", "", "", "", ""]
                file_write.write(pad_cells(category_cells, "|"))
                file_write.write(pad_cells_row_dividers("-"))
                for simulation in category.simulations:
                    file_write.write(pad_cells(simulation.get_row(), "|"))
                    file_write.write(pad_cells_row_dividers("-"))

if __name__ == "__main__":
    generate_table()

# Steps to follow:
# 1. Delete table from `../docs/source/simulation_locations.rst`.
# 2. Run `python generate_table.py`
# 3. Copy the output of `cat simulation_table.txt` to `../docs/source/simulation_locations.rst`.
# 4. `cd ../docs/ && make html`
# 5. `rm -rf /global/cfs/cdirs/e3sm/www/forsyth/data_docs`
# 6. `mv _build /global/cfs/cdirs/e3sm/www/forsyth/data_docs`
# 7. `chmod -R o+r /global/cfs/cdirs/e3sm/www/forsyth/data_docs`
# 8. `chmod -R o+x /global/cfs/cdirs/e3sm/www/forsyth/data_docs`
# 9. Go to https://portal.nersc.gov/project/e3sm/forsyth/data_docs/html/simulation_locations.html
