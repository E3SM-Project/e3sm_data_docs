resolution=LR
for case_name in amip_0301; do
  ./generate_reproduction_script.bash ${resolution} ${case_name}
  diff ../run_scripts/v2/reproduce/run.v2.${resolution}.${case_name}.sh run.v2.${resolution}.${case_name}.sh
  mv run.v2.${resolution}.${case_name}.sh ../run_scripts/v2/reproduce/run.v2.${resolution}.${case_name}.sh
done

#resolution=NARRM
#for case_name in amip_0101 amip_0201 amip_0301; do
#  ./generate_reproduction_script.bash ${resolution} ${case_name}
#  diff ../run_scripts/v2/reproduce/run.v2.${resolution}.${case_name}.sh run.v2.${resolution}.${case_name}.sh
#  mv run.v2.${resolution}.${case_name}.sh ../run_scripts/v2/reproduce/run.v2.${resolution}.${case_name}.sh
#done
