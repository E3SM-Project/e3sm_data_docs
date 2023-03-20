resolution=LR
for case_name in piControl abrupt-4xCO2_0101 abrupt-4xCO2_0301 1pctCO2_0101 historical_0101 historical_0151 historical_0201 historical_0251 historical_0301 historical_0101_bonus hist-GHG_0101 hist-GHG_0201 hist-GHG_0251 hist-GHG_0301 hist-aer_0101 hist-aer_0201 hist-aer_0251 hist-aer_0301 hist-all-xGHG-xaer_0101 hist-all-xGHG-xaer_0201 hist-all-xGHG-xaer_0251 hist-all-xGHG-xaer_0301 amip_0101 amip_0201 amip_0301 amip_0101_bonus piClim-control piClim-histall_0021 piClim-histall_0041 piClim-histaer_0021 piClim-histaer_0041; do
  ./generate_reproduction_script.bash ${resolution} ${case_name}
  diff ../run_scripts/v2/reproduce/run.v2.${resolution}.${case_name}.sh run.v2.${resolution}.${case_name}.sh
  mv run.v2.${resolution}.${case_name}.sh ../run_scripts/v2/reproduce/run.v2.${resolution}.${case_name}.sh
done

resolution=NARRM
for case_name in historical_0101 historical_0301 amip_0101 amip_0201 amip_0301; do
  ./generate_reproduction_script.bash ${resolution} ${case_name}
  diff ../run_scripts/v2/reproduce/run.v2.${resolution}.${case_name}.sh run.v2.${resolution}.${case_name}.sh
  mv run.v2.${resolution}.${case_name}.sh ../run_scripts/v2/reproduce/run.v2.${resolution}.${case_name}.sh
done
