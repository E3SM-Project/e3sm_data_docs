# TODO: Restore to all scripts before merging
resolution=LR
for case_name in historical_0101_bonus amip_0301 amip_0101_bonus; do
  ./generate_reproduction_script.bash ${resolution} ${case_name}
  diff ../run_scripts/v2/reproduce/run.v2.${resolution}.${case_name}.sh run.v2.${resolution}.${case_name}.sh
  mv run.v2.${resolution}.${case_name}.sh ../run_scripts/v2/reproduce/run.v2.${resolution}.${case_name}.sh
done

resolution=NARRM
for case_name in abrupt-4xCO2_0101 1pctCO2_0101 amip_0101 amip_0201 amip_0301; do
  ./generate_reproduction_script.bash ${resolution} ${case_name}
  diff ../run_scripts/v2/reproduce/run.v2.${resolution}.${case_name}.sh run.v2.${resolution}.${case_name}.sh
  mv run.v2.${resolution}.${case_name}.sh ../run_scripts/v2/reproduce/run.v2.${resolution}.${case_name}.sh
done
