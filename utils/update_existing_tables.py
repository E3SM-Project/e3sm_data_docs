#!/usr/bin/env python
"""
Regenerate all existing simulation tables, then cross-check them against
CMIP6-Metadata.

Steps:
  1. For every csv in `input/` other than the AI training data, run
     `generate_tables.construct_pages` once per (model_version, group) pair
     found in that csv. (E.g. `simulations_v2_1.csv` contains both the
     WaterCycle and BGC groups, so it produces two calls.)
  2. Run `generate_tables.generate_ai_training_table` on the AI training csv.
  3. Run `metadata_reviewer.main()`, which reads the freshly generated
     `simulation_table.rst` pages.

Run this from the directory containing `generate_tables.py`, e.g.:
    python update_existing_tables.py
(`generate_tables` writes to `../docs/...` and `../machine_readable_data/...`
relative to the current working directory, so the script changes into its own
directory before doing anything.)
"""

import csv
import os
import sys
import traceback
from collections import OrderedDict
from pathlib import Path
from typing import List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
INPUT_DIR = "input"
AI_TRAINING_CSV = "ai_training_data.csv"
AI_TRAINING_OUTPUT = "../docs/source/AITraining/simulation_data/simulation_table.rst"

# `generate_tables` uses paths relative to the cwd, so make that predictable
# (and make sure `generate_tables` / `metadata_reviewer` are importable).
os.chdir(SCRIPT_DIR)
sys.path.insert(0, str(SCRIPT_DIR))

import generate_tables  # noqa: E402
import metadata_reviewer  # noqa: E402


def find_model_version_group_pairs(csv_file: Path) -> List[Tuple[str, str]]:
    """Return the distinct (model_version, group) pairs in a simulations csv,
    in order of first appearance.

    This is a cheap read of just those two columns -- it deliberately does not
    construct `Simulation` objects, since that triggers `hsi` / network calls.
    """
    pairs: "OrderedDict[Tuple[str, str], None]" = OrderedDict()
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        if reader.fieldnames is None:
            return []
        reader.fieldnames = [name.strip() for name in reader.fieldnames]
        if "model_version" not in reader.fieldnames or "group" not in reader.fieldnames:
            raise RuntimeError(
                f"{csv_file} is missing a 'model_version' and/or 'group' column"
            )
        for row in reader:
            model_version = (row.get("model_version") or "").strip()
            group = (row.get("group") or "").strip()
            if model_version and group:
                pairs[(model_version, group)] = None
    return list(pairs)


def main() -> int:
    failures: List[str] = []

    csv_files = sorted(Path(INPUT_DIR).glob("*.csv"))
    if not csv_files:
        print(f"No csv files found in {Path(INPUT_DIR).resolve()}")
        return 1

    for csv_file in csv_files:
        if csv_file.name == AI_TRAINING_CSV:
            continue  # Handled separately below.
        try:
            pairs = find_model_version_group_pairs(csv_file)
            if not pairs:
                print(f"Skipping {csv_file}: no simulations found")
                continue
            for model_version, group_name in pairs:
                print(f"\n=== {csv_file}: {model_version} {group_name} ===")
                try:
                    generate_tables.construct_pages(
                        str(csv_file), model_version, group_name
                    )
                except Exception:
                    traceback.print_exc()
                    failures.append(f"{csv_file} ({model_version} {group_name})")
        except Exception:
            traceback.print_exc()
            failures.append(str(csv_file))

    # AI training datasets (different layout, different generator)
    ai_csv = Path(INPUT_DIR) / AI_TRAINING_CSV
    if ai_csv.exists():
        print(f"\n=== {ai_csv}: AI training datasets ===")
        try:
            generate_tables.generate_ai_training_table(str(ai_csv), AI_TRAINING_OUTPUT)
        except Exception:
            traceback.print_exc()
            failures.append(str(ai_csv))
    else:
        print(f"\nWARNING: {ai_csv} not found; skipping AI training table")

    # Cross-check against CMIP6-Metadata (reads the tables generated above)
    print("\n=== Running metadata_reviewer ===")
    try:
        metadata_reviewer.main()
    except Exception:
        traceback.print_exc()
        failures.append("metadata_reviewer")

    if failures:
        print("\nFinished with failures:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("\nAll tables updated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
