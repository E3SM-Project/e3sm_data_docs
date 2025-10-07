***************
Simulation Data 
***************

The E3SMv2 simulation data is available on **ESGF** and **NERSC HPSS**.

The preferred retrieval method is **ESGF**. Native output is available at `ESGF <https://esgf-node.llnl.gov/search/e3sm/?model_version=2_0>`_, and a subset of the data is reformatted to conform to CMIP conventions and submmited to the CMIP6 ESGF archive (ESGF links are provided in the table below for published data).

Additionally, all native model output data has also been archived on **NERSC HPSS** using `zstash <https://e3sm-project.github.io/zstash>`_.

**If you have an account on NERSC**, you can retrieve the data locally or remotely using Globus.

To download simulation data locally on a NERSC machine: ::

   zstash extract --hpss=<HPSS path in table>

To download simulation data remotely using the zstash Globus interface: ::

   zstash extract --hpss=globus://nersc/<HPSS path in table>

or ::

   zstash extract --hpss=globus://9cd89cfd-6d04-11e5-ba46-22000b92c6ec/<HPSS path below>

Note that the data management tool `zstash <https://github.com/E3SM-Project/zstash>`_ is available from the `E3SM-Unified <https://github.com/E3SM-Project/e3sm-unified>`_ conda environment. An example of retrieving all **eam.h0** (monthly atmosphere output files) between **years 0030 and 0049** for the v2.LR.piControl simulation at NERSC locally is demonstrated as below in two steps:

1. To activate E3SM-Unified environment by:
   ::

    source /global/common/software/e3sm/anaconda_envs/load_latest_e3sm_unified_pm-cpu.sh

2. To retrieve files with zstash command:
   ::

    zstash extract --hpss=/home/projects/e3sm/www/WaterCycle/E3SMv2/LR/v2.LR.piControl "*.elm.h0.00[3-4]?-??.nc"


For more information, refer to `zstash usage <https://e3sm-project.github.io/zstash/_build/html/master/usage.html#extract>`_. 


**If you do not have access to NERSC**, you can download simulation data directly through the  NERSC HPSS
`web interface <https://portal.nersc.gov/archive/home/projects/e3sm/www/WaterCycle/E3SMv2>`_.
Note that this will be slow and inefficient since you'll have to download the tar files.

**Tip for users without NERSC access**: Before downloading large tar files, you can first download the ``index.db`` file and use sqlite to check the archive contents: ::

   sqlite3 index.db "SELECT tar,name,size from files;" > archive_contents.txt

This will help you identify which specific tar files contain the data you need before downloading.

**v2.LR** simulations data has been archived on NERSC HPSS under: ::

  /home/projects/e3sm/www/WaterCycle/E3SMv2/LR

and **v2.NARRM** simulations data under: ::

  /home/projects/e3sm/www/WaterCycle/E3SMv2/NARRM


Scripts to reproduce v2 simulations are available `here <https://github.com/E3SM-Project/e3sm_data_docs/tree/main/run_scripts/v2/reproduce/>`_
with specific instructions details in `Reproducing Simulations`.
Original run scripts (the scripts that were originally used to create the simulations) have been archived here `here <https://github.com/E3SM-Project/e3sm_data_docs/tree/main/run_scripts/v2/original/>`_. These latter scripts are provided for reference only.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   simulation_table