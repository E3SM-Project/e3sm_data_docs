import os
import re

class Simulation(object):
    def __init__(self, directory):
        self.name = directory.rsplit("/")[-1]
        self.directory = directory
        output = "out.txt"
        os.system(f'(hsi "du {directory}") 2>&1 | tee {output}')
        with open(output, "r") as f:
            for line in f:
                match_object = re.search("\((.*) bytes\)", line) 
                if match_object:
                    num_bytes = match_object.group(1).replace(",", "")
                    break
        self.size = int(num_bytes)
        self.tb = int(num_bytes)/1e12

    def display(self):
        #print(" "*6 + f"{self.name}: {self.size:e} bytes")
        print(" "*6 + f"{self.name}: {self.tb:.0f} TB")

class Category(object):
    def __init__(self, name, simulations):
        self.name = name
        self.simulations = simulations
        self.count = len(simulations)
        size = 0
        for simulation in self.simulations:
            size += simulation.size
        self.size = size
        self.tb = size/1e12

    def display(self):
        #print(" "*4 + f"{self.name}: {self.count} members, {self.size:e} bytes")
        print(" "*4 + f"{self.name}: {self.count} members, {self.tb:.0f} TB")
        for simulation in self.simulations:
            simulation.display()

class Resolution(object):
    def __init__(self, name, categories):
        self.name = name
        self.categories = categories
        count = 0
        size = 0
        for category in self.categories:
            count += category.count
            size += category.size
        self.count = count
        self.size = size
        self.tb = size/1e12

    def display(self):
        #print(" "*2 + f"{self.name}: {self.count} members, {self.size:e} bytes")
        print(" "*2 + f"{self.name}: {self.count} members, {self.tb:.0f} TB")
        for category in self.categories:
            category.display()

class TotalArchive(object):
    def __init__(self, name, resolutions):
        self.name = name
        self.resolutions = resolutions
        count = 0
        size = 0
        for resolution in self.resolutions:
            count += resolution.count
            size += resolution.size
        self.count = count
        self.size = size
        self.tb = size/1e12

    def display(self):
        #print(f"{self.name}: {self.count} members, {self.size:e} bytes")
        print(f"{self.name}: {self.count} members, {self.tb:.0f} TB")
        for resolution in self.resolutions:
            resolution.display()

def make_sims_list(directories):
    return list(map(Simulation, directories))

def print_sizes():
    simulations = make_sims_list([
        "/home/g/golaz/E3SMv2/v2.LR.piControl",
        "/home/g/golaz/E3SMv2/v2.LR.piControl_land",
        "/home/g/golaz/E3SMv2/v2.LR.abrupt-4xCO2_0101",
        "/home/g/golaz/E3SMv2/v2.LR.abrupt-4xCO2_0301",
        "/home/g/golaz/E3SMv2/v2.LR.1pctCO2_0101",
    ])
    deck = Category("DECK", simulations)
    simulations = make_sims_list([
        "/home/f/forsyth/E3SMv2/v2.LR.historical_0101",
        "/home/f/forsyth/E3SMv2/v2.LR.historical_0151",
        "/home/f/forsyth/E3SMv2/v2.LR.historical_0201",
        "/home/f/forsyth/E3SMv2/v2.LR.historical_0251",
        "/home/f/forsyth/E3SMv2/v2.LR.historical_0301",
    ])
    historical = Category("Historical", simulations)
    simulations = make_sims_list([
        "/home/g/golaz/E3SMv2/v2.LR.historical_0111",
        "/home/g/golaz/E3SMv2/v2.LR.historical_0121",
        "/home/g/golaz/E3SMv2/v2.LR.historical_0131",
        "/home/g/golaz/E3SMv2/v2.LR.historical_0141",
        "/home/g/golaz/E3SMv2/v2.LR.historical_0161",
        "/home/g/golaz/E3SMv2/v2.LR.historical_0171",
        "/home/g/golaz/E3SMv2/v2.LR.historical_0181",
        "/home/g/golaz/E3SMv2/v2.LR.historical_0191",
        "/home/g/golaz/E3SMv2/v2.LR.historical_0211",
        "/home/g/golaz/E3SMv2/v2.LR.historical_0221",
        "/home/g/golaz/E3SMv2/v2.LR.historical_0231",
        "/home/g/golaz/E3SMv2/v2.LR.historical_0241",
        "/home/g/golaz/E3SMv2/v2.LR.historical_0261",
        "/home/g/golaz/E3SMv2/v2.LR.historical_0271",
        "/home/g/golaz/E3SMv2/v2.LR.historical_0281",
        "/home/g/golaz/E3SMv2/v2.LR.historical_0291",
    ])
    historical_le = Category("Historical LE", simulations)
    simulations = make_sims_list([
        "/home/x/xzheng/E3SMv2/v2.LR.hist-GHG_0101",
        "/home/g/golaz/E3SMv2/v2.LR.hist-GHG_0151",
        "/home/f/forsyth/E3SMv2/v2.LR.hist-GHG_0201",
        "/home/f/forsyth/E3SMv2/v2.LR.hist-GHG_0251",
        "/home/g/golaz/E3SMv2/v2.LR.hist-GHG_0301",
        "/home/x/xzheng/E3SMv2/v2.LR.hist-aer_0101",
        "/home/g/golaz/E3SMv2/v2.LR.hist-aer_0151",
        "/home/f/forsyth/E3SMv2/v2.LR.hist-aer_0201",
        "/home/f/forsyth/E3SMv2/v2.LR.hist-aer_0251",
        "/home/g/golaz/E3SMv2/v2.LR.hist-aer_0301",
        "/home/x/xzheng/E3SMv2/v2.LR.hist-all-xGHG-xaer_0101",
        "/home/g/golaz/E3SMv2/v2.LR.hist-all-xGHG-xaer_0151",
        "/home/f/forsyth/E3SMv2/v2.LR.hist-all-xGHG-xaer_0201",
        "/home/f/forsyth/E3SMv2/v2.LR.hist-all-xGHG-xaer_0251",
        "/home/g/golaz/E3SMv2/v2.LR.hist-all-xGHG-xaer_0301",
    ])
    single_forcing = Category("Single-forcing (DAMIP-like)", simulations)
    simulations = make_sims_list([
        "/home/f/forsyth/E3SMv2/v2.LR.amip_0101",
        "/home/f/forsyth/E3SMv2/v2.LR.amip_0201",
        "/home/f/forsyth/E3SMv2/v2.LR.amip_0301",
    ])
    amip = Category("AMIP", simulations)
    simulations = make_sims_list([
        "/home/g/golaz/E3SMv2/v2.LR.piClim-control",
        "/home/g/golaz/E3SMv2/v2.LR.piClim-histall_0021",
        "/home/g/golaz/E3SMv2/v2.LR.piClim-histall_0031",
        "/home/f/forsyth/E3SMv2/v2.LR.piClim-histall_0041",
        "/home/g/golaz/E3SMv2/v2.LR.piClim-histaer_0021",
        "/home/g/golaz/E3SMv2/v2.LR.piClim-histaer_0031",
        "/home/f/forsyth/E3SMv2/v2.LR.piClim-histaer_0041"
    ])
    rfmip = Category("RFMIP", simulations)
    low_res = Resolution("Water Cycle (low-resolution)", [deck, historical, historical_le, single_forcing, amip, rfmip])
    simulations = make_sims_list([
        "/home/t/tang30/E3SMv2/v2.NARRM.piControl",
        "/home/g/golaz/E3SMv2/v2.NARRM.abrupt-4xCO2_0101",
        "/home/g/golaz/E3SMv2/v2.NARRM.1pctCO2_0101",
    ])
    deck = Category("DECK", simulations)
    simulations = make_sims_list([
        "/home/t/tang30/E3SMv2/v2.NARRM.historical_0101",
        "/home/g/golaz/E3SMv2/v2.NARRM.historical_0301",
    ])
    historical = Category("Historical", simulations)
    simulations = make_sims_list([
        "/home/t/tang30/E3SMv2/v2.NARRM.amip_0101",
        "/home/t/tang30/E3SMv2/v2.NARRM.amip_0201",
    ])
    amip = Category("AMIP", simulations)
    narrm = Resolution("Water Cycle (NARRM)", [deck, historical, amip])
    total = TotalArchive("TOTAL", [low_res, narrm])
    total.display()
    

if __name__ == "__main__":
    print_sizes()
