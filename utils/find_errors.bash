#!/bin/bash

for case_name in v2.LR.abrupt-4xCO2_0301 v2.LR.hist-GHG_0201 v2.LR.hist-GHG_0251 v2.LR.hist-GHG_0301 v2.LR.hist-aer_0201 v2.LR.hist-aer_0251 v2.LR.hist-aer_0301 v2.LR.hist-all-xGHG-xaer_0201 v2.LR.hist-all-xGHG-xaer_0251 v2.LR.hist-all-xGHG-xaer_0301 v2.LR.amip_0201 v2.LR.amip_0301
do
  echo "######################################################################"
  cd /lcrc/group/e3sm/${USER}/E3SMv2_test/${case_name}/tests/XS_1x10_ndays/run
  echo "/lcrc/group/e3sm/${USER}/E3SMv2_test/${case_name}/tests/XS_1x10_ndays/run"
  zgrep error *log*
done
