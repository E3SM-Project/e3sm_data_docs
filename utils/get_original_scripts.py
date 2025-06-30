import csv
import shutil
from pathlib import Path
from typing import List

# Initially generated with LivChat

def get_model_names(csv_path: str) -> List[str]:
    print("Entering get_model_names")
    model_names: List[str] = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip header
        for row in reader:
            if len(row) >= 6:
                model_name: str = row[4].strip()

                # Extract machine name
                machine: str = row[5].strip()
                if f".{machine}" in model_name:
                    # Ends with machine name
                    model_name = model_name.replace(f".{machine}", "")
                elif f"{machine}." in model_name:
                    # Starts with machine name
                    model_name = model_name.replace(f"{machine}.", "")
                
                model_names.append(model_name)
                print(f"Will look for: {model_name}")
    return model_names

def find_original_run_scripts(original_run_script_dir: str, model_names: List[str]) -> List[Path]:
    print("Entering find_original_run_scripts")
    matches: List[str] = []
    root = Path(original_run_script_dir)
    for file_path in root.rglob('*'):
        if file_path.is_file():
            if any(model_name in file_path.name for model_name in model_names):
                matches.append(file_path)
                print(f"Match: {file_path}")
    return matches

def copy_files_preserving_structure(files: List[Path], src_root: str, dest_root: str):
    print("Entering copy_files_preserving_structure")
    src_root = Path(src_root)
    dest_root = Path(dest_root)
    for file_path in files:
        relative_path = file_path.relative_to(src_root)
        dest_path = dest_root / relative_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Copying {file_path} to {dest_path}")
        shutil.copy2(file_path, dest_path)

if __name__ == "__main__":
    csv_file = "/global/homes/f/forsyth/ez/e3sm_data_docs/utils/simulations_v1_water_cycle.csv"
    search_directory = '/global/homes/f/forsyth/SimulationScripts/archive/'
    destination_directory = '/global/homes/f/forsyth/ez/e3sm_data_docs/run_scripts/v1/original/'

    model_names: List[str] = get_model_names(csv_file)
    matching_files: List[Path] = find_original_run_scripts(search_directory, model_names)
    copy_files_preserving_structure(matching_files, search_directory, destination_directory)
