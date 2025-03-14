***************
Simulation Data 
***************

The E3SMv2.1 simulation data is available on **ESGF** and **NERSC HPSS**. Please note that the BGC numbering system gives ``v2.1`` simulations a prefix of ``v2``.

The data is reformatted to conform to CMIP conventions and was submmited to the CMIP6 ESGF archive. (ESGF links are provided in the table below for published data).

Additionally, all native model output data has also been archived on **NERSC HPSS** using `zstash <https://e3sm-project.github.io/zstash>`_.

**If you have an account on NERSC**, you can retrieve the data locally or remotely using Globus.

To download simulation data locally on a NERSC machine: ::

   zstash extract --hpss=<HPSS path below>

To download simulation data remotely using the zstash Globus interface: ::

   zstash extract --hpss=globus://nersc/<HPSS path below>

or ::

   zstash extract --hpss=globus://9cd89cfd-6d04-11e5-ba46-22000b92c6ec/<HPSS path below>

Note that the data management tool `zstash <https://github.com/E3SM-Project/zstash>`_ is available from the `E3SM-Unified <https://github.com/E3SM-Project/e3sm-unified>`_ conda environment. An example of retrieving all **elm.h0** (monthly land output files) between **years 1930 and 1949** for the v2.LR.BGC-LNDATM.CONTRL simulation at NERSC locally is demonstrated as below in two steps:

1. To activate E3SM-Unified environment by:
   ::

    source /global/common/software/e3sm/anaconda_envs/load_latest_e3sm_unified_pm-cpu.sh

2. To retrieve files with zstash command:
   ::

    zstash extract --hpss=/home/projects/e3sm/www/BGC/E3SMv2_1/v2.LR.BGC-LNDATM.CONTRL/ "*.elm.h0.19[3-4]?-??.nc"


For more information, refer to `zstash usage <https://e3sm-project.github.io/zstash/_build/html/master/usage.html#extract>`_. 


**If you do not have access to NERSC**, you can download simulation data directly through the  NERSC HPSS
`web interface <https://portal.nersc.gov/archive/home/projects/e3sm/www/BGC/E3SMv2_1>`_.
Note that this will be slow and inefficient since you'll have to download the tar files.

**v2_1.LR** simulations data has been archived on NERSC HPSS under: ::

  /home/projects/e3sm/www/BGC/E3SMv2_1


Original run scripts can be found `here <https://github.com/E3SM-Project/e3sm_data_docs/tree/main/run_scripts/v2.1/original>`_.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   simulation_table
