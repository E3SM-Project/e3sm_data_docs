#!/bin/bash

#SBATCH  --job-name=test_reproduction_scripts
#SBATCH  --account=e3sm
#SBATCH  --nodes=1
#SBATCH  --output=test_reproduction_scripts.o%j
#SBATCH  --exclusive
#SBATCH  --time=24:00:00
#SBATCH  --partition=compute

# Run with `sbatch test_reproduction_scripts.bash`

# https://stackoverflow.com/questions/19456518/invalid-command-code-despite-escaping-periods-using-sed
# `replace_in_file x y f` will replace all appearances of `x` with `y` in the file `f`.
replace_in_file()
{
  sed -i "s/$1/$2/" $3
}

test_reproduction()
{
  # Change this if you want to use a different subdirectory name for testing.
  test_subdir=$1
  # Choose the resolution and simulation name from the "Simulation" column on https://e3sm-project.github.io/e3sm_data_docs/_build/html/v2/reproducing_simulations.html
  resolution=$2
  simulation_name=$3
  # Change this to `false` if you already have E3SM checked out.
  do_fetch_code=$4
  # Change this to `false` if the script is not in the Github repository.
  use_wget=$5
  
  #####
  # (1) Retrieve run script
  mkdir -p ~/${test_subdir}/scripts
  cd ~/${test_subdir}/scripts
  case_name=v2.${resolution}.${simulation_name}
  script_name=run.${case_name}.sh
  # Start with fresh slate
  rm ~/${test_subdir}/scripts/${script_name}
  rm -rf /lcrc/group/e3sm/${USER}/${test_subdir}/${case_name}
  if [ "$use_wget" == "true" ]; then
    # The Github address is what's linked in the "Script" column on https://e3sm-project.github.io/e3sm_data_docs/_build/html/v2/reproducing_simulations.html
    github_address=https://raw.githubusercontent.com/E3SM-Project/e3sm_data_docs/main/run_scripts/v2/reproduce/${script_name}
    wget ${github_address}
  else
    cp /home/ac.forsyth2/e3sm_data_docs/run_scripts/v2/reproduce/${script_name} ${script_name}
  fi
  replace_in_file "E3SMv2_test" ${test_subdir} ${script_name}
  # Variable substitution in the string doesn't appear to work in this case, so using `if` statement.
  if [ "$do_fetch_code" == "false" ]; then
    replace_in_file "do_fetch_code=true" "do_fetch_code=false" ${script_name}
  fi

  # (2) Retrieve initial conditions from NERSC HPSS
  mkdir -p /lcrc/group/e3sm/${USER}/${test_subdir}/${case_name}
  cd /lcrc/group/e3sm/${USER}/E3SMv2_test/${case_name}
  # Note: if this line fails, you may need to extract the init from a different case.
  # Check the `RUN_REFDIR` in the reproduction script to see what case should be referenced.
  # You can either manually edit this line, or just run the appropriate `zstash extract` command before running this script.
  zstash extract -v --hpss=globus://nersc/home/projects/e3sm/www/WaterCycle/E3SMv2/${resolution}/${case_name} "init/*"
  # Remove zstash cache
  rm -rf zstash

  # (3) Compile and run test
  cd ~/${test_subdir}/scripts
  chmod 755 ${script_name}
  # This eventually launches a job on another compute node, but the compile step happens on this node.
  # Running test_reproduction_scripts.bash from a compute node means the compile step will not use a log-in node.
  ./${script_name}

  echo "If ${script_name} did not complete successfully, try the following:"
  echo "Make fixes in /home/ac.forsyth2/e3sm_data_docs/run_scripts/v2/reproduce/${script_name}"
  echo "Set use_wget=false"
}

# Load E3SM unified to make zstash available
source /lcrc/soft/climate/e3sm-unified/load_latest_e3sm_unified_chrysalis.sh

### Usual run ###

# Water Cycle (low-resolution) > DECK
for simulation_name in piControl abrupt-4xCO2_0101 abrupt-4xCO2_0301 1pctCO2_0101; do
  test_reproduction E3SMv2_test LR ${simulation_name} false false
done

# Water Cycle (low-resolution) > Historical
for simulation_name in historical_0101 historical_0151 historical_0201 historical_0251 historical_0301 historical_0101_bonus; do
  test_reproduction E3SMv2_test LR ${simulation_name} false false
done

# Water Cycle (low-resolution) > Single-forcing (DAMIP-like)
for simulation_name in hist-GHG_0101 hist-GHG_0201 hist-GHG_0251 hist-GHG_0301 hist-aer_0101 hist-aer_0201 hist-aer_0251 hist-aer_0301 hist-all-xGHG-xaer_0101 hist-all-xGHG-xaer_0201 hist-all-xGHG-xaer_0251 hist-all-xGHG-xaer_0301; do
  test_reproduction E3SMv2_test LR ${simulation_name} false false
done

# Water Cycle (low-resolution) > AMIP
for simulation_name in amip_0101 amip_0201 amip_0301 amip_0101_bonus; do
  test_reproduction E3SMv2_test LR ${simulation_name} false false
done

# Water Cycle (low-resolution) > RFMIP
for simulation_name in piClim-control piClim-histall_0021 piClim-histall_0041 piClim-histaer_0021 piClim-histaer_0041; do
  test_reproduction E3SMv2_test LR ${simulation_name} false false
done

# Water Cycle (NARRM) > DECK
for simulation_name in piControl abrupt-4xCO2_0101 1pctCO2_0101; do
  test_reproduction E3SMv2_test NARRM ${simulation_name} false false
done

# Water Cycle (NARRM) > Historical
for simulation_name in historical_0101 historical_0301; do
  test_reproduction E3SMv2_test NARRM ${simulation_name} false false
done

# Water Cycle (NARRM) > AMIP
for simulation_name in amip_0101 amip_0201 amip_0301; do
  test_reproduction E3SMv2_test NARRM ${simulation_name} false false
done
