import csv
import os
import re
from typing import List, Tuple

# Run with `time python find_data.py > out_find_data.txt`

# Standard HPSS `/home/projects/e3sm/www/WaterCycle/E3SMv1/` paths from
# https://docs.e3sm.org/e3sm_data_docs/_build/html/v1/WaterCycle/simulation_data/simulation_table.html
CENTRALIZED_PREFIXES: List[str] = [
    "/home/projects/e3sm/www/WaterCycle/E3SMv1/LR/",
    "/home/projects/e3sm/www/WaterCycle/E3SMv1/HR/"
]
# User-specific paths from
# https://e3sm.atlassian.net/wiki/spaces/ED/pages/4495441922/V1+Simulation+backfill+WIP
USER_PREFIXES: List[str] = [
    "/home/b/beharrop/E3SM_simulations/",
    "/home/c/chengzhu/",
    "/home/d/dcomeau/cryosphere_simulations/",
    "/home/g/golaz/2018/E3SM_simulations/",
    "/home/g/golaz/2018/E3SM_simulations/repaired/",
    "/home/g/golaz/2019/E3SM_simulations/",
    "/home/g/golaz/2019/E3SM_simulations/repaired/",
    "/home/j/jinyun/CBGCv1/",
    "/home/j/jonbob/",
    "/home/m/maltrud/E3SM/",
    "/home/n/ndk/2019/",
    "/home/n/ndk/2020/",
    "/home/n/ndk/2021/",
    "/home/projects/m3412/"
    "/home/s/shix/E3SM/",
    "/home/t/tang30/2018/E3SM_simulations/",
    "/home/t/tang30/2018/E3SM_simulations/repaired/",
    "/home/t/tang30/2019/E3SM_simulations/",
    "/home/t/tang30/2019/E3SM_simulations/repaired/",
    "/home/q/qzhu/CBGCv1/",
    "/home/z/zshaheen/2018/E3SM_simulations/",
    "/home/z/zshaheen/2018/E3SM_simulations/repaired/",
]
# Publication paths `/home/projects/e3sm/www/publication-archives/` noted in
# https://github.com/E3SM-Project/e3sm_data_docs/pull/59#issuecomment-3063668732
PUBLICATION_PREFIXES: List[str] = [
    "/home/projects/e3sm/www/publication-archives/pub_archive_E3SM_1_0_"
]

class DataPathsContainer(object):
    def __init__(self, simulation_name: str):
        self.simulation_name: str = simulation_name
        self.real_paths: List[str] = []
        self.symlink_paths: List[Tuple[str, str]] = [] # (x, y) => x symlinks to y, the real path

    def get_num_total_copies(self) -> int:
        return len(self.real_paths) + len(self.symlink_paths)
    
    def get_num_hard_copies(self) -> int:
        return len(self.real_paths)


def read_simulations(csv_file: str) -> List[DataPathsContainer]:
    with open(csv_file, newline='') as opened_file:
        reader = csv.reader(opened_file)
        header: List[str] = []
        simulation_name_index: int = 4
        containers: List[DataPathsContainer] = []
        for row in reader:
            if header == []:
                for label in row:
                    header.append(label.strip())
                if "simulation_name" not in header:
                    raise RuntimeError(f"Cannot find simulation names in {csv_file}")
                else:
                    simulation_name_index = header.index("simulation_name")
            else: 
                if len(row) != len(header):
                    raise RuntimeError(f"header has {len(header)} labels, but row={row} has {len(row)} entries")
                containers.append(DataPathsContainer(row[simulation_name_index].strip()))
    return containers

def search_for_all_appearances(containers: List[DataPathsContainer]):
    num_prefixes: int = len(CENTRALIZED_PREFIXES) + len (USER_PREFIXES) + len(PUBLICATION_PREFIXES)
    num_simulations: int = len(containers)
    print(f"Trying {num_prefixes} paths for {num_simulations} simulations ({num_prefixes * num_simulations} combinations)")
    for container in containers:
        for prefix in CENTRALIZED_PREFIXES:
            add_hpss_paths(container, prefix)
        for prefix in USER_PREFIXES:
            add_hpss_paths(container, prefix)
        for prefix in PUBLICATION_PREFIXES:
            add_hpss_paths(container, prefix)

def add_hpss_paths(container: DataPathsContainer, hpss_prefix: str):
    output: str = "out_hsi_ls_l.txt"
    if os.path.exists(output):
        os.remove(output)
    hpss_path: str = f"{hpss_prefix}{container.simulation_name}"
    os.system(f'(hsi "ls -l {hpss_path}") 2>&1 | tee {output}')
    with open(output, "r") as f:
        for line in f:
            match_object = re.search(f"ls: No such file or directory", line)
            if match_object:
                # The simulation isn't at this path
                return
            match_object = re.search(f"{container.simulation_name}@ -> (.+)$", line)
            if match_object:
                symlink_dst: str = match_object.group(1)
                container.symlink_paths.append((hpss_path, symlink_dst))
                return
    # We didn't find any evidence the path doesn't exist or any evidence that it's a symlink
    container.real_paths.append(hpss_path)

def construct_markdown_table(containers: List[DataPathsContainer]):
    output_file: str = "out_simulation_paths.md"
    with open(output_file, "w") as f:
        f.write("# Data Paths\n\n")
        f.write("| Simulation name | Physically present in this many places | Accessible from this many places | Physically in publication archives? | Accessible from centralized location? | Real paths | Symlink paths |\n")
        f.write("| --- | --- | --- | --- | --- | --- | --- |\n")
        for container in containers:
            physically_in_publication_archive: bool = False
            accessible_from_central_location: bool = False
            symlinks: List[str] = []
            for (src, dst) in container.symlink_paths:
                symlinks.append(f"{src} -> {dst}")
                if not physically_in_publication_archive:
                    physically_in_publication_archive = check_for_prefix(dst, PUBLICATION_PREFIXES)
                if not accessible_from_central_location:
                    accessible_from_central_location = check_for_prefix(src, CENTRALIZED_PREFIXES)
            if not physically_in_publication_archive:
                for path in container.real_paths:
                    physically_in_publication_archive = check_for_prefix(path, PUBLICATION_PREFIXES)
                    if physically_in_publication_archive:
                        break
            if not accessible_from_central_location:
                for path in container.real_paths:
                    accessible_from_central_location = check_for_prefix(path, CENTRALIZED_PREFIXES)
                    if accessible_from_central_location:
                        break
            f.write(f"| {container.simulation_name} | {container.get_num_hard_copies()} | {container.get_num_total_copies()} | {bool2str(physically_in_publication_archive)} | {bool2str(accessible_from_central_location)} | {container.real_paths} | {symlinks} |\n")

def check_for_prefix(path: str, prefix_list: List[str]):
    for prefix in prefix_list:
        if path.startswith(prefix):
            return True
    return False

def bool2str(val: bool) -> str:
    if val:
        return "Yes"
    else:
        return "" # Empty string

if __name__ == "__main__":
    containers: List[DataPathsContainer] = read_simulations("input/simulations_v1_water_cycle.csv")
    search_for_all_appearances(containers)
    construct_markdown_table(containers)
