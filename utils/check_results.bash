#!/bin/bash

failed_line_count=0
failed_checksum=0

check_test_results()
{
  # Change this if you want to use a different subdirectory name for testing.
  test_subdir=$1
  # Choose the resolution and simulation name from the "Simulation" column on https://e3sm-project.github.io/e3sm_data_docs/_build/html/v2/reproducing_simulations.html
  resolution=$2
  simulation_name=$3
  # Set this to be the value from the "10 day checksum" column on https://e3sm-project.github.io/e3sm_data_docs/_build/html/v2/reproducing_simulations.html
  checksum=$4

  #####
  case_name=v2.${resolution}.${simulation_name}
  echo ''
  echo ${case_name}

  # (4) After the job completed, check results
  cd /lcrc/group/e3sm/${USER}/${test_subdir}/${case_name}/tests
  for test in *_*_ndays
  do
    gunzip -c ${test}/run/atm.log.*.gz | grep '^ nstep, te ' | uniq > atm_${test}.txt
  done
  actual_line_count=`wc -l atm_*.txt`
  # 482 lines, corresponding to 10 simulated days
  expected_line_count="482 atm_XS_1x10_ndays.txt"
  if [ "${actual_line_count}" == "${expected_line_count}" ]; then
    echo "Line count test passed"
  else
    echo "Line count test failed"  
    echo ${actual_line_count}
    echo ${expected_line_count}
    ((failed_line_count++))
    echo "Debug:"
    echo "/lcrc/group/e3sm/${USER}/${test_subdir}/${case_name}/tests"
  fi
  actual_checksum=`md5sum atm_*.txt`
  expected_checksum="${checksum}  atm_XS_1x10_ndays.txt"
  # If the checksums match, the results are BFB with the original code.
  if [ "${actual_checksum}" == "${expected_checksum}" ]; then
    echo "Checksum test passed"
  else
    echo "Checksum test failed"
    echo ${actual_checksum}
    echo ${expected_checksum}
    ((failed_checksum++))
    echo "Debug:"
    echo "/lcrc/group/e3sm/${USER}/${test_subdir}/${case_name}/tests"
  fi
}

# Water Cycle (low-resolution) > DECK
check_test_results E3SMv2_test LR piControl 7547932242025fdf92014d06d6f9eec2
check_test_results E3SMv2_test LR abrupt-4xCO2_0101 86bc7dfbdc6a71e4bd2925943a15c474
check_test_results E3SMv2_test LR abrupt-4xCO2_0301 cd61cc01cfbd03913fafcb6cbe18a8bc
check_test_results E3SMv2_test LR 1pctCO2_0101 3300255fc76bc13433fafea37fb36570
# Water Cycle (low-resolution) > Historical
check_test_results E3SMv2_test LR historical_0101 61a7f492bdcc6e6cd4a2b41c92546219
check_test_results E3SMv2_test LR historical_0151 6b17c91b7e07d31c162adbfbe7782d42
check_test_results E3SMv2_test LR historical_0201 e79dda36bb76507cc6fdf88292e8ced9
check_test_results E3SMv2_test LR historical_0251 6ad002ff6f198f6ba936171da48bc5b2
check_test_results E3SMv2_test LR historical_0301 42ffbf170db587dc25d84d5d2ec7bc12
check_test_results E3SMv2_test LR historical_0101_bonus d23e455ba5bef0bf87211468570b6835
# Water Cycle (low-resolution) > Single-forcing (DAMIP-like)
check_test_results E3SMv2_test LR hist-GHG_0101 5cc8d0d76887740d8a82568e13e2ff36
check_test_results E3SMv2_test LR hist-GHG_0201 9098a4135bfda91ccef99d3f701fd5e5
check_test_results E3SMv2_test LR hist-GHG_0251 7924e97a4abf55bbd7be708987e29153
check_test_results E3SMv2_test LR hist-GHG_0301 d461a8bbddd3afc9f8d701943609b83c
check_test_results E3SMv2_test LR hist-aer_0101 c00ea4f726194ced3669a7f0ae0bac27
check_test_results E3SMv2_test LR hist-aer_0201 7feaa4d32a7a888ff969106e48ed9db7
check_test_results E3SMv2_test LR hist-aer_0251 849376c7d30ad2dd296f4b4e16eeccf0
check_test_results E3SMv2_test LR hist-aer_0301 d35d92f676c4b312e227415cf19b3316
check_test_results E3SMv2_test LR hist-all-xGHG-xaer_0101 a5768c505bb12f778b2606ae8f5705ce
check_test_results E3SMv2_test LR hist-all-xGHG-xaer_0201 363ecb08227bdfd972e5f058dd12b434
check_test_results E3SMv2_test LR hist-all-xGHG-xaer_0251 6a9465b94bef49a235defbd44db273bd
check_test_results E3SMv2_test LR hist-all-xGHG-xaer_0301 16a900d361d1edcbd24813445d7d1cd6
# Water Cycle (low-resolution) > AMIP
check_test_results E3SMv2_test LR amip_0101 a6cff5ea277dd3a08be6bbc4b1c84a69
check_test_results E3SMv2_test LR amip_0201 64e0fae59c1f6a48da0cae534c8be4a1
check_test_results E3SMv2_test LR amip_0301 6ae0ba340ef42b945c8573e9e5d7a0c7
check_test_results E3SMv2_test LR amip_0101_bonus c4b1c7337e89134fca7420437992ea97
# Water Cycle (low-resolution) > RFMIP
check_test_results E3SMv2_test LR piClim-control 6ce41c36ea2f86e984d12d364085323e
check_test_results E3SMv2_test LR piClim-histall_0021 c932625975561731c96124c4b3105b44
check_test_results E3SMv2_test LR piClim-histall_0041 0e9d9fbc8a132299fed161bd833fdd43
check_test_results E3SMv2_test LR piClim-histaer_0021 442ebb4ff467d8c9f57c5d5b4ec37bd9
check_test_results E3SMv2_test LR piClim-histaer_0041 a67cf4f46aa6ca5f568b5a14f0b2f887
# Water Cycle (NARRM) > DECK
check_test_results E3SMv2_test NARRM piControl c18df3c0834abd2b5c63899e37559ccd
check_test_results E3SMv2_test NARRM abrupt-4xCO2_0101 1eb5423d852764bbcd1bf67b180efc43
check_test_results E3SMv2_test NARRM 1pctCO2_0101 80e6c83b39d58cb00876506deabfd8c2
# Water Cycle (NARRM) > Historical
check_test_results E3SMv2_test NARRM historical_0101 4a9ccd61766640b4a4f4b15dc5f5b956
check_test_results E3SMv2_test NARRM historical_0301 24147fbb5d601e1bd6fcae6ace72968c
# Water Cycle (NARRM) > AMIP
check_test_results E3SMv2_test NARRM amip_0101 930b7fc7e946910c3c8e716f733d0f31
check_test_results E3SMv2_test NARRM amip_0201 a8326dd3922cbf32dccedb494fcedffb
check_test_results E3SMv2_test NARRM amip_0301 f8bcd50a7e9c5ef8253908b73ee7471c

echo ""
echo "Failed line count:"
echo $failed_line_count
echo "Failed checksum:"
echo $failed_checksum
