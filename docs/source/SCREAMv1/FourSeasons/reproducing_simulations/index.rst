***********************
Reproducing Simulations 
***********************

All **v2.LR** simulations were run on E3SM's **chrysalis** cluster. Most **v2.NARRM** were run on chrysalis
as well, except for three historical members that were run on **NERSC cori-knl**.

Original simulations can be reproduced BFB (bit-for-bit) on the same machines. While you can 
rerun simulations on a different machines as well, the results with not be BFB due to hardware and software differences.

Below are detailed instructions on how to reproduce **v2.LR.piControl** on **chrysalis**. It
should be reasonably simple to adapt for other simulations and/or machines.

Files are usually stored in two locatations: scripts and source code in the home file system (~/E3SMv2_test)
and model files in the scratch file syatem (/lcrc/group/e3sm/$USER/E3SMv2_test). ::

  # Load E3SM unified to make zstash available
  source /lcrc/soft/climate/e3sm-unified/load_latest_e3sm_unified_chrysalis.sh
  # Replace with the case you're running.
  # CASE_NAME is what's listed in the "Simulation" column below.
  CASE_NAME="v2.LR.piControl"

  # (1) Retrieve run script
  mkdir -p ~/E3SMv2_test/scripts
  cd ~/E3SMv2_test/scripts
  # The Github address is what's listed in the "Script" column below.
  wget https://raw.githubusercontent.com/E3SM-Project/e3sm_data_docs/main/run_scripts/v2/reproduce/run.v2.LR.piControl.sh
  vi run.${CASE_NAME}.sh
  #--> customize as needed
  # If you named your directory, something other than "E3SMv2_test",
  # you'll need to update those references in this script.
  # If you already have compiled code, set: `do_fetch_code=false`
  
  # (2) Retrieve initial conditions from NERSC HPSS
  mkdir -p /lcrc/group/e3sm/${USER}/E3SMv2_test/${CASE_NAME}
  cd /lcrc/group/e3sm/${USER}/E3SMv2_test/${CASE_NAME}
  # If you're reproducing a NAARM run, replace the "LR" with "NARRM"
  zstash extract -v --hpss=globus://nersc/home/projects/e3sm/www/WaterCycle/E3SMv2/LR/${CASE_NAME} "init/*"

  # Remove zstash cache
  rm -rf zstash

  # (3) Compile and run test
  cd ~/E3SMv2_test/scripts
  ./run.${CASE_NAME}.sh

  # (4) After the job completed, check resuls
  cd /lcrc/group/e3sm/${USER}/E3SMv2_test/${CASE_NAME}/tests
  for test in *_*_ndays
  do
    gunzip -c ${test}/run/atm.log.*.gz | grep '^ nstep, te ' | uniq > atm_${test}.txt
  done
  wc -l atm_*.txt
  482 atm_XS_1x10_ndays.txt
  #--> each should have 482 lines, corresponding to 10 simulated days
  md5sum atm_*.txt
  7547932242025fdf92014d06d6f9eec2  atm_XS_1x10_ndays.txt
  # Checksum matches reference simulation (see "10 day checksum" column below),
  # so results are BFB with original code.
  
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   reproduction_table