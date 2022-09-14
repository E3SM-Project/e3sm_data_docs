import csv
import os
import re
import requests

class Simulation(object):
    def __init__(self, name):
        self.name = name
        
        hpss_path = f"/home/projects/e3sm/www/WaterCycle/E3SMv2/LR/{name}"
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

        run_script_original = f"https://github.com/E3SM-Project/e3sm_data_docs/tree/main/run_scripts/original/run.{name}.sh"
        response = requests.get(run_script_original).status_code
        if response == 200:
            self.run_script_original = f"`{name} <{run_script_original}>`_"
        else:
            self.run_script_original = ""

        self.run_script_reproduction = "TBD"

    def get_row(self):
        return [self.name, self.data_size, self.hpss, self.run_script_original, self.run_script_reproduction]


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
    simulation_names = [
        "v2.LR.piControl",
        "v2.LR.piControl_land",
        "v2.LR.abrupt-4xCO2_0101",
        "v2.LR.abrupt-4xCO2_0301",
        "v2.LR.1pctCO2_0101",
    ]
    for simulation_name in simulation_names:
        deck.append(Simulation(simulation_name))

    historical = Category("Historical")
    low_res.append(historical)
    simulation_names = [
        "v2.LR.historical_0101",
        "v2.LR.historical_0151",
        "v2.LR.historical_0201",
        "v2.LR.historical_0251",
        "v2.LR.historical_0301",
        "v2.LR.historical_0101_bonus",
    ]
    for simulation_name in simulation_names:
        historical.append(Simulation(simulation_name))

    historical_le = Category("Historical LE")
    low_res.append(historical_le)
    simulation_names = [
        "v2.LR.historical_0111",
        "v2.LR.historical_0121",
        "v2.LR.historical_0131",
        "v2.LR.historical_0141",
        "v2.LR.historical_0161",
        "v2.LR.historical_0171",
        "v2.LR.historical_0181",
        "v2.LR.historical_0191",
        "v2.LR.historical_0211",
        "v2.LR.historical_0221",
        "v2.LR.historical_0231",
        "v2.LR.historical_0241",
        "v2.LR.historical_0261",
        "v2.LR.historical_0271",
        "v2.LR.historical_0281",
        "v2.LR.historical_0291",
    ]
    for simulation_name in simulation_names:
        historical_le.append(Simulation(simulation_name))

    single_forcing = Category("Single-forcing (DAMIP-like)")
    low_res.append(single_forcing)
    simulation_names = [
        "v2.LR.hist-GHG_0101",
        "v2.LR.hist-GHG_0151",
        "v2.LR.hist-GHG_0201",
        "v2.LR.hist-GHG_0251",
        "v2.LR.hist-GHG_0301",
        "v2.LR.hist-aer_0101",
        "v2.LR.hist-aer_0151",
        "v2.LR.hist-aer_0201",
        "v2.LR.hist-aer_0251",
        "v2.LR.hist-aer_0301",
        "v2.LR.hist-all-xGHG-xaer_0101",
        "v2.LR.hist-all-xGHG-xaer_0151",
        "v2.LR.hist-all-xGHG-xaer_0201",
        "v2.LR.hist-all-xGHG-xaer_0251",
        "v2.LR.hist-all-xGHG-xaer_0301",
    ]
    for simulation_name in simulation_names:
        single_forcing.append(Simulation(simulation_name))


    amip = Category("AMIP")
    low_res.append(amip)
    simulation_names = [
        "v2.LR.amip_0101",
        "v2.LR.amip_0201",
        "v2.LR.amip_0301",
        "v2.LR.amip_0101_bonus",
    ]
    for simulation_name in simulation_names:
        amip.append(Simulation(simulation_name))

    rfmip = Category("RFMIP")
    low_res.append(rfmip)
    simulation_names = [
        "v2.LR.piClim-control",
        "v2.LR.piClim-histall_0021",
        "v2.LR.piClim-histall_0031",
        "v2.LR.piClim-histall_0041",
        "v2.LR.piClim-histaer_0021",
        "v2.LR.piClim-histaer_0031",
        "v2.LR.piClim-histaer_0041",
    ]
    for simulation_name in simulation_names:
        rfmip.append(Simulation(simulation_name))

    rrm = Resolution("Water Cycle (NARRM)")

    deck = Category("DECK")
    rrm.append(deck)
    simulation_names = [
        "v2.NARRM.piControl",
        "v2.NARRM.abrupt-4xCO2_0101",
        "v2.NARRM.1pctCO2_0101",
    ]
    for simulation_name in simulation_names:
        deck.append(Simulation(simulation_name))

    historical = Category("Historical")
    rrm.append(historical)
    simulation_names = [
        "v2.NARRM.historical_0101",
        "v2.NARRM.historical_0151",
        "v2.NARRM.historical_0201",
        "v2.NARRM.historical_0251",
        "v2.NARRM.historical_0301",
        "v2.NARRM.historical_0101_bonus",
    ]
    for simulation_name in simulation_names:
        historical.append(Simulation(simulation_name))

    amip = Category("AMIP")
    rrm.append(amip)
    simulation_names = [
        "v2.NARRM.amip_0101",
        "v2.NARRM.amip_0201",
        "v2.NARRM.amip_0301",
        "v2.NARRM.amip_0101_bonus",
    ]
    for simulation_name in simulation_names:
        amip.append(Simulation(simulation_name))
        
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
    string += f" {cells[2]:<80} " + col_divider
    string += f" {cells[3]:<200} " + col_divider
    string += f" {cells[4]:<25} " + col_divider
    string += "\n"
    return string

def pad_cells_row_dividers(marker):
    string = "+"
    string += marker*67 + "+"
    string += marker*17 + "+"
    string += marker*82 + "+"
    string += marker*202 + "+"
    string += marker*27 + "+"
    string += "\n"
    return string

def generate_table():
    resolution_list = create_simulation_objects()
    header_cells = ["Simulation", "Data Size (TB)", "HPSS Path", "Original Run Script", "Reproduction Run Script"]
    with open("simulation_table.txt", "w") as file_write:
        file_write.write(pad_cells_row_dividers("-"))
        file_write.write(pad_cells(header_cells, "|"))
        file_write.write(pad_cells_row_dividers("="))
        for resolution in resolution_list:
            for category in resolution.categories:
                category_cells = [f"**{resolution.name} > {category.name}**", "", "", "", ""]
                file_write.write(pad_cells(category_cells, "|"))
                file_write.write(pad_cells_row_dividers("-"))
                for simulation in category.simulations:
                    file_write.write(pad_cells(simulation.get_row(), "|"))
                    file_write.write(pad_cells_row_dividers("-"))

if __name__ == "__main__":
    generate_table()

# Steps to follow:
# 1. Run `python generate_table.py`
# 2. Copy the output of `cat simulation_table.txt` to `e3sm_data_docs/docs/source/simulation_locations.rst`.
# 3. `cd e3sm_data_docs/docs/`
# 4.`make html`

# 5. `rm -rf /lcrc/group/e3sm/public_html/diagnostic_output/ac.forsyth2/data_docs`
# 6. `mv _build /lcrc/group/e3sm/public_html/diagnostic_output/ac.forsyth2/data_docs`
# 7. Go to https://web.lcrc.anl.gov/public/e3sm/diagnostic_output/ac.forsyth2/data_docs/html/simulation_locations.html

# 5. `rm -rf /global/cfs/cdirs/e3sm/www/forsyth/data_docs`
# 6. `mv _build /global/cfs/cdirs/e3sm/www/forsyth/data_docs`
# 7. `chmod -R o+r /global/cfs/cdirs/e3sm/www/forsyth/data_docs`
# 8. `chmod -R o+x /global/cfs/cdirs/e3sm/www/forsyth/data_docs`
# 9. Go to https://portal.nersc.gov/project/e3sm/forsyth/data_docs/html/simulation_locations.html