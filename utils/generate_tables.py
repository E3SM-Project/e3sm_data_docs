import csv
import os
import re
import requests

class Simulation(object):
    def __init__(self, name, resolution, machine, checksum, experiment=None, ensemble_num=None):
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

        # For simulation_table.txt
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

        run_script_original = f"https://github.com/E3SM-Project/e3sm_data_docs/tree/main/run_scripts/v2/original/run.{name}.sh"
        response = requests.get(run_script_original).status_code
        if response == 200:
            self.run_script_original = f"`{name} <{run_script_original}>`_"
        else:
            self.run_script_original = ""

        # For reproduction_table.txt
        self.machine = machine
        self.checksum = checksum

        run_script_reproduction = f"https://raw.githubusercontent.com/E3SM-Project/e3sm_data_docs/main/run_scripts/v2/reproduce/run.{name}.sh"
        response = requests.get(run_script_reproduction).status_code
        if response == 200:
            self.run_script_reproduction = f"`{name} <{run_script_reproduction}>`_"
        else:
            self.run_script_reproduction = ""

    def get_row(self, output_file):
        if output_file == "simulation_table.txt":
            return [self.name, self.data_size, self.esgf, self.hpss]
        elif output_file == "reproduction_table.txt":
            return [self.name, self.machine, self.run_script_reproduction, self.checksum]
        else:
            raise RuntimeError(f"Invalid output_file={output_file}")


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
        ("v2.LR.piControl","LR", "chrysalis", "7547932242025fdf92014d06d6f9eec2", "piControl", 1),
        ("v2.LR.piControl_land", "LR", "chrysalis", "", None, None),
        ("v2.LR.abrupt-4xCO2_0101", "LR", "chrysalis", "86bc7dfbdc6a71e4bd2925943a15c474", "abrupt-4xCO2", 1),
        ("v2.LR.abrupt-4xCO2_0301", "LR", "chrysalis", "86bc7dfbdc6a71e4bd2925943a15c474", "abrupt-4xCO2", 2),
        ("v2.LR.1pctCO2_0101", "LR", "chrysalis", "3300255fc76bc13433fafea37fb36570", "1pctCO2", 1),
    ]
    for simulation_tuple in simulation_tuples:
        deck.append(Simulation(*simulation_tuple))

    historical = Category("Historical")
    low_res.append(historical)
    simulation_tuples = [
        ("v2.LR.historical_0101", "LR", "chrysalis", "61a7f492bdcc6e6cd4a2b41c92546219", "historical", 1),
        ("v2.LR.historical_0151", "LR", "chrysalis", "6b17c91b7e07d31c162adbfbe7782d42", "historical", 2),
        ("v2.LR.historical_0201", "LR", "chrysalis", "e79dda36bb76507cc6fdf88292e8ced9", "historical", 3),
        ("v2.LR.historical_0251", "LR", "chrysalis", "6ad002ff6f198f6ba936171da48bc5b2", "historical", 4),
        ("v2.LR.historical_0301", "LR", "chrysalis", "42ffbf170db587dc25d84d5d2ec7bc12", "historical", 5),
        ("v2.LR.historical_0101_bonus", "LR", "chrysalis", "d23e455ba5bef0bf87211468570b6835", None, None),
    ]
    for simulation_tuple in simulation_tuples:
        historical.append(Simulation(*simulation_tuple))

    historical_le = Category("Historical LE")
    low_res.append(historical_le)
    simulation_tuples = [
        ("v2.LR.historical_0111", "LR", "cori-knl", ""),
        ("v2.LR.historical_0121", "LR", "cori-knl", ""),
        ("v2.LR.historical_0131", "LR", "cori-knl", ""),
        ("v2.LR.historical_0141", "LR", "cori-knl", ""),
        ("v2.LR.historical_0161", "LR", "cori-knl", ""),
        ("v2.LR.historical_0171", "LR", "cori-knl", ""),
        ("v2.LR.historical_0181", "LR", "cori-knl", ""),
        ("v2.LR.historical_0191", "LR", "cori-knl", ""),
        ("v2.LR.historical_0211", "LR", "cori-knl", ""),
        ("v2.LR.historical_0221", "LR", "cori-knl", ""),
        ("v2.LR.historical_0231", "LR", "cori-knl", ""),
        ("v2.LR.historical_0241", "LR", "cori-knl", ""),
        ("v2.LR.historical_0261", "LR", "cori-knl", ""),
        ("v2.LR.historical_0271", "LR", "cori-knl", ""),
        ("v2.LR.historical_0281", "LR", "cori-knl", ""),
        ("v2.LR.historical_0291", "LR", "cori-knl", ""),
    ]
    for simulation_tuple in simulation_tuples:
        historical_le.append(Simulation(*simulation_tuple))

    single_forcing = Category("Single-forcing (DAMIP-like)")
    low_res.append(single_forcing)
    simulation_tuples = [
        ("v2.LR.hist-GHG_0101", "LR", "chrysalis", "5cc8d0d76887740d8a82568e13e2ff36", "hist-GHG", 1),
        ("v2.LR.hist-GHG_0151", "LR", "chrysalis", "", "hist-GHG", 2),
        ("v2.LR.hist-GHG_0201", "LR", "chrysalis", "5cc8d0d76887740d8a82568e13e2ff36", "hist-GHG", 3),
        ("v2.LR.hist-GHG_0251", "LR", "chrysalis", "5cc8d0d76887740d8a82568e13e2ff36", "hist-GHG", 4),
        ("v2.LR.hist-GHG_0301", "LR", "chrysalis", "5cc8d0d76887740d8a82568e13e2ff36", "hist-GHG", 5),
        ("v2.LR.hist-aer_0101", "LR", "chrysalis", "c00ea4f726194ced3669a7f0ae0bac27", "hist-aer", 1),
        ("v2.LR.hist-aer_0151", "LR", "chrysalis", "", "hist-aer", 2),
        ("v2.LR.hist-aer_0201", "LR", "chrysalis", "c00ea4f726194ced3669a7f0ae0bac27", "hist-aer", 3),
        ("v2.LR.hist-aer_0251", "LR", "chrysalis", "c00ea4f726194ced3669a7f0ae0bac27", "hist-aer", 4),
        ("v2.LR.hist-aer_0301", "LR", "chrysalis", "c00ea4f726194ced3669a7f0ae0bac27", "hist-aer", 5),
        ("v2.LR.hist-all-xGHG-xaer_0101", "LR", "chrysalis", "a5768c505bb12f778b2606ae8f5705ce", None, None),
        ("v2.LR.hist-all-xGHG-xaer_0151", "LR", "chrysalis", "", None, None),
        ("v2.LR.hist-all-xGHG-xaer_0201", "LR", "chrysalis", "a5768c505bb12f778b2606ae8f5705ce", None, None),
        ("v2.LR.hist-all-xGHG-xaer_0251", "LR", "chrysalis", "a5768c505bb12f778b2606ae8f5705ce", None, None),
        ("v2.LR.hist-all-xGHG-xaer_0301", "LR", "chrysalis", "a5768c505bb12f778b2606ae8f5705ce", None, None),
    ]
    for simulation_tuple in simulation_tuples:
        single_forcing.append(Simulation(*simulation_tuple))


    amip = Category("AMIP")
    low_res.append(amip)
    simulation_tuples = [
        ("v2.LR.amip_0101", "LR", "chrysalis", "a6cff5ea277dd3a08be6bbc4b1c84a69", "amip", 1),
        ("v2.LR.amip_0201", "LR", "chrysalis", "64e0fae59c1f6a48da0cae534c8be4a1", "amip", 2),
        ("v2.LR.amip_0301", "LR", "chrysalis", "6ae0ba340ef42b945c8573e9e5d7a0c7", "amip", 3),
        ("v2.LR.amip_0101_bonus", "LR", "chrysalis", "c4b1c7337e89134fca7420437992ea97", None, None)
    ]
    for simulation_tuple in simulation_tuples:
        amip.append(Simulation(*simulation_tuple))

    rfmip = Category("RFMIP")
    low_res.append(rfmip)
    simulation_tuples = [
        ("v2.LR.piClim-control", "LR", "chrysalis", "6ce41c36ea2f86e984d12d364085323e", "piClim-control", 1),
        ("v2.LR.piClim-histall_0021", "LR", "chrysalis", "c932625975561731c96124c4b3105b44", "piClim-histall", 1),
        ("v2.LR.piClim-histall_0031", "LR", "chrysalis", "", "piClim-histall", 2),
        ("v2.LR.piClim-histall_0041", "LR", "chrysalis", "0e9d9fbc8a132299fed161bd833fdd43", "piClim-histall", 3),
        ("v2.LR.piClim-histaer_0021", "LR", "chrysalis", "442ebb4ff467d8c9f57c5d5b4ec37bd9", "piClim-histaer", 1),
        ("v2.LR.piClim-histaer_0031", "LR", "chrysalis", "", "piClim-histaer", 2),
        ("v2.LR.piClim-histaer_0041", "LR", "chrysalis", "a67cf4f46aa6ca5f568b5a14f0b2f887", "piClim-histaer", 3)
    ]
    for simulation_tuple in simulation_tuples:
        rfmip.append(Simulation(*simulation_tuple))

    other = Category("Other")
    low_res.append(other)
    simulation_tuples = [
        ("v2_ndgclim_t6h_1850aer", "LR", "", ""),
        ("v2_ndgclim_t6h_2010aer", "LR", "", ""),
    ]
    for simulation_tuple in simulation_tuples:
        other.append(Simulation(*simulation_tuple))

    rrm = Resolution("Water Cycle (NARRM)")

    deck = Category("DECK")
    rrm.append(deck)
    simulation_tuples = [
        ("v2.NARRM.piControl", "NARRM", "chrysalis", "c18df3c0834abd2b5c63899e37559ccd"),
        ("v2.NARRM.abrupt-4xCO2_0101", "NARRM", "chrysalis", "1eb5423d852764bbcd1bf67b180efc43"),
        ("v2.NARRM.1pctCO2_0101", "NARRM", "chrysalis", "80e6c83b39d58cb00876506deabfd8c2"),
    ]
    for simulation_tuple in simulation_tuples:
        deck.append(Simulation(*simulation_tuple))

    historical = Category("Historical")
    rrm.append(historical)
    simulation_tuples = [
        ("v2.NARRM.historical_0101", "NARRM", "chrysalis", "4a9ccd61766640b4a4f4b15dc5f5b956"),
        ("v2.NARRM.historical_0151", "NARRM", "cori-knl", ""),
        ("v2.NARRM.historical_0201", "NARRM", "cori-knl", ""),
        ("v2.NARRM.historical_0251", "NARRM", "cori-knl", ""),
        ("v2.NARRM.historical_0301", "NARRM", "chrysalis", "24147fbb5d601e1bd6fcae6ace72968c"),
        ("v2.NARRM.historical_0101_bonus", "NARRM", "chrysalis", ""),
    ]
    for simulation_tuple in simulation_tuples:
        historical.append(Simulation(*simulation_tuple))

    amip = Category("AMIP")
    rrm.append(amip)
    simulation_tuples = [
        ("v2.NARRM.amip_0101", "NARRM", "chrysalis", "930b7fc7e946910c3c8e716f733d0f31"),
        ("v2.NARRM.amip_0201", "NARRM", "chrysalis", "a8326dd3922cbf32dccedb494fcedffb"),
        ("v2.NARRM.amip_0301", "NARRM", "chrysalis", "f8bcd50a7e9c5ef8253908b73ee7471c"),
        ("v2.NARRM.amip_0101_bonus", "NARRM", "chrysalis", ""),
    ]
    for simulation_tuple in simulation_tuples:
        amip.append(Simulation(*simulation_tuple))

    other = Category("Other")
    rrm.append(other)
    simulation_tuples = [
        ("v2.NA.F20TR.6h.f1.1850aer", "NARRM", "", ""),
        ("v2.NA.F20TR.6h.f1.2010aer", "NARRM", "", ""),
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
                    
def generate_table(resolution_list, header_cells, output_file, cell_paddings):
    with open(output_file, "w") as file_write:
        # Table Header
        file_write.write(pad_cells_row_dividers("-", cell_paddings))
        file_write.write(pad_cells(header_cells, "|", cell_paddings))
        file_write.write(pad_cells_row_dividers("=", cell_paddings))
        # Table Body
        for resolution in resolution_list:
            for category in resolution.categories:
                # Category rows
                category_cells = [""]*len(header_cells)
                category_cells[0] = f"**{resolution.name} > {category.name}**"
                file_write.write(pad_cells(category_cells, "|", cell_paddings))
                file_write.write(pad_cells_row_dividers("-", cell_paddings))
                for simulation in category.simulations:
                    # Simulation rows
                    file_write.write(pad_cells(simulation.get_row(output_file), "|", cell_paddings))
                    file_write.write(pad_cells_row_dividers("-", cell_paddings))

def main():
    resolution_list = create_simulation_objects()
    generate_table(
        resolution_list,
        ["Simulation", "Data Size (TB)", "ESGF Link", "HPSS Path"],
        "simulation_table.txt",
        [65, 15, 150, 80]
    )
    generate_table(
        resolution_list,
        ["Simulation", "Machine", "Script", "10 day checksum"],
        "reproduction_table.txt",
        [65, 11, 200, 34]
    )
                    
if __name__ == "__main__":
    main()
