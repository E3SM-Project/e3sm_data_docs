resolution=LR
for case_name in hist-GHG_0151 hist-aer_0151 hist-all-xGHG-xaer_0151 piClim-histall_0031 piClim-histaer_0031; do
  ./generate_reproduction_script.bash ${resolution} ${case_name}
  diff ../run_scripts/v2/reproduce/run.v2.${resolution}.${case_name}.sh run.v2.${resolution}.${case_name}.sh
  mv run.v2.${resolution}.${case_name}.sh ../run_scripts/v2/reproduce/run.v2.${resolution}.${case_name}.sh
done

resolution=NARRM
for case_name in historical_0151 historical_0201 historical_0251; do
  ./generate_reproduction_script.bash ${resolution} ${case_name}
  diff ../run_scripts/v2/reproduce/run.v2.${resolution}.${case_name}.sh run.v2.${resolution}.${case_name}.sh
  mv run.v2.${resolution}.${case_name}.sh ../run_scripts/v2/reproduce/run.v2.${resolution}.${case_name}.sh
done
