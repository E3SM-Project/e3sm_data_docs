rm compare_diffs.txt
for case in piControl abrupt-4xCO2_0101 1pctCO2_0101 1pctCO2_0101 historical_0301; do
  diff ../run_scripts/v2/original/run.v2.NARRM.${case}.sh ../run_scripts/v2/reproduce/run.v2.LR.${case}.sh >> compare_diffs.txt
done
grep -A 1 "readonly CHECKOUT" compare_diffs.txt
