***********************
Reproducing Simulations 
***********************

All **v2.LR** simulations were run on E3SM's **chrysalis** cluster. Most **v2.NARRM** were run on chrysalis
as well, except for three historical members that were run on **NERSC cori-knl**.

Original simulations can be reproduced BFB (bit-for-bit) on the same machines. While you can 
rerun simulations on a different machines as well, the results with not be BFB due to hardware and software differences.

Below are details instructions on how to reproduce **v2.LR.piControl** on **chrysalis**. It
should be reasonably simple to adapt for other simulations and/or machines.

Files are usually stored in two locatations: scripts and source code in the home file system (~/E3SMv2_test)
and model file in the scratch file syatem (/lcrc/group/e3sm/$USER/E3SMv2_test). ::

  # Load E3SM unified to make zstash available
  source /lcrc/soft/climate/e3sm-unified/load_latest_e3sm_unified_chrysalis.sh

  # (1) Retrieve run script
  mkdir -p ~/E3SMv2_test/scripts
  cd ~/E3SMv2_test/scripts
  wget <github address>
  vi run.v2.LR.piControl.sh
  #--> customize as needed
  
  # (2) Retrieve initial conditions from NERSC HPSS
  CASE_NAME="v2.LR.piControl"
  mkdir -p /lcrc/group/e3sm/${USER}/E3SMv2_test/${CASE_NAME}
  cd /lcrc/group/e3sm/${USER}/E3SMv2_test/${CASE_NAME}
  zstash extract -v --hpss=globus://nersc/home/projects/e3sm/www/WaterCycle/E3SMv2/LR/v2.LR.piControl "init/*"

  # Remove zstash cache
  rm -rf zstash

  # (3) Compile and run test
  cd ~/E3SMv2_test/scripts
  ./run.v2.LR.piControl.sh

  # (4) After the job completed, check resuls
  cd /lcrc/group/e3sm/ac.golaz/E3SMv2_test/v2.LR.piControl/tests
  for test in *_*_ndays
  do
    gunzip -c ${test}/run/atm.log.*.gz | grep '^ nstep, te ' | uniq > atm_${test}.txt
  done
  wc -l atm_*.txt
  482 atm_XS_1x10_ndays.txt
  #--> each should have 482 lines, corresponding to 10 simulated days
  md5sum atm_*.txt
  7547932242025fdf92014d06d6f9eec2  atm_XS_1x10_ndays.txt
  #--> OK, checksum matches refrence simulation, so results are BFB with original code.
  
The table below provides link to scripts, original machine and md5 checksum for the original
E3SMv2 simulations:

+-----------------+-----------+------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+
| Simulation      | Machine   | Script                                                                                                                             | 10 day checksum                   |
+=================+===========+====================================================================================================================================+===================================+
| v2.LR.piControl | chrysalis | `run.v2.LR.piControl.sh <https://github.com/E3SM-Project/e3sm_data_docs/tree/main/run_scripts/reproduce/run.v2.LR.piControl.sh>`_  | 7547932242025fdf92014d06d6f9eec2a |
+-----------------+-----------+------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+
|                 |           |                                                                                                                                    |                                   |
+-----------------+-----------+------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+



