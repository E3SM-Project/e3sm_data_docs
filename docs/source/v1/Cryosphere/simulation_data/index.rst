***************
Simulation Data 
***************

The E3SMv1 simulation data is available on **NERSC HPSS**.

All native model output data has also been archived on **NERSC HPSS** using `zstash <https://e3sm-project.github.io/zstash>`_.

**If you have an account on NERSC**, you can retrieve the data locally or remotely using Globus.

To download simulation data locally on a NERSC machine: ::

   zstash extract --hpss=<HPSS path in table>

To download simulation data remotely using the zstash Globus interface: ::

   zstash extract --hpss=globus://nersc/<HPSS path in table>

or ::

   zstash extract --hpss=globus://9cd89cfd-6d04-11e5-ba46-22000b92c6ec/<HPSS path below>

Note that the data management tool `zstash <https://github.com/E3SM-Project/zstash>`_ is available from the `E3SM-Unified <https://github.com/E3SM-Project/e3sm-unified>`_ conda environment. An example of retrieving all **mpaso.hist.am.meridionalHeatTransport** between **years 0003 and 0004** for the "CORE-IAF with ice shelf melt fluxes" simulation at NERSC locally is demonstrated as below in two steps:

1. To activate E3SM-Unified environment by:
   ::

    source /global/common/software/e3sm/anaconda_envs/load_latest_e3sm_unified_pm-cpu.sh

2. To retrieve files with zstash command:
   ::

    zstash extract --hpss=/home/projects/e3sm/www/Cryosphere/E3SMv1/20190225.GMPAS-DIB-IAF-ISMF.T62_oEC60to30v3wLI.cori-knl "*mpaso.hist.am.meridionalHeatTransport.000[3-4]-??-??.nc"


For more information, refer to `zstash usage <https://e3sm-project.github.io/zstash/_build/html/master/usage.html#extract>`_. 


**If you do not have access to NERSC**, you can download simulation data directly through the  NERSC HPSS
`web interface <https://portal.nersc.gov/archive/home/projects/e3sm/www/Cryosphere/E3SMv1>`_.
Note that this will be slow and inefficient since you'll have to download the tar files.

Simulation data has been archived on NERSC HPSS under: ::

  /home/projects/e3sm/www/Cryosphere/E3SMv1


Scripts are not available to reproduce v1 simulations.

Original run scripts are also not available in the `archive <https://github.com/E3SM-Project/e3sm_data_docs/tree/main/run_scripts/v1/original/>`_. A few methods to search for run scripts, in general: ::

  # Try looking directly
  zstash ls --hpss=/home/projects/e3sm/www/Cryosphere/E3SMv1/<simulation_name>/ case_scripts/run_script_provenance/*

  # Try looking for provenance or run
  zstash ls --hpss=/home/projects/e3sm/www/Cryosphere/E3SMv1/<simulation_name> > out.txt
  grep -in provenance out.txt
  grep -in run out.txt


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   simulation_table
