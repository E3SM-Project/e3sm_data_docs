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

Note that the data management tool `zstash <https://github.com/E3SM-Project/zstash>`_ is available from the `E3SM-Unified <https://github.com/E3SM-Project/e3sm-unified>`_ conda environment. An example of retrieving all **cam.h0** (monthly atmosphere output files) between **years 0030 and 0049** for the piControl simulation at NERSC locally is demonstrated as below in two steps:

1. To activate E3SM-Unified environment by:
   ::

    source /global/common/software/e3sm/anaconda_envs/load_latest_e3sm_unified_pm-cpu.sh

2. To retrieve files with zstash command:
   ::

    zstash ls --hpss=/home/projects/e3sm/www/BGC/E3SMv1/E3SM_1_1_piControl "*.cam.h3.18[5-6]?-??-??-?????.nc"


For more information, refer to `zstash usage <https://e3sm-project.github.io/zstash/_build/html/master/usage.html#extract>`_. 


**If you do not have access to NERSC**, you can download simulation data directly through the  NERSC HPSS
`web interface <https://portal.nersc.gov/archive/home/projects/e3sm/www/BGC/E3SMv1>`_.
Note that this will be slow and inefficient since you'll have to download the tar files.

**v1.LR** simulations data has been archived on NERSC HPSS under: ::

  /home/projects/e3sm/www/BGC/E3SMv1/LR

and **v1.HR** simulations data under: ::

  /home/projects/e3sm/www/BGC/E3SMv1/HR


Scripts are not available to reproduce v1 simulations.

Some original run scripts (the scripts that were originally used to create the simulations) have been archived here `here <https://github.com/E3SM-Project/e3sm_data_docs/tree/main/run_scripts/v1/original/>`_. If a script is not collected here, you can try looking for the provenance run script with:
  ::

   zstash extract --hpss=/home/projects/e3sm/www/BGC/E3SMv1/<simulation_name>/ case_scripts/run_script_provenance/*

In the table below, there are 6 main categories of data:

* `CTC CMIP piControl <https://esgf-node.llnl.gov/search/cmip6/?activity_id=CMIP&source_id=E3SM-1-1&experiment_id=piControl>`_
* `CTC C4MIP hist-bgc <https://esgf-node.llnl.gov/search/cmip6/?activity_id=C4MIP&source_id=E3SM-1-1&experiment_id=hist-bgc>`_
* `CTC C4MIP ssp585-bgc <https://esgf-node.llnl.gov/search/cmip6/?activity_id=C4MIP&source_id=E3SM-1-1&experiment_id=ssp585-bgc>`_
* `ECA CMIP piControl <https://esgf-node.llnl.gov/search/cmip6/?activity_id=CMIP&source_id=E3SM-1-1-ECA&experiment_id=piControl>`_
* `ECA C4MIP hist-bgc <https://esgf-node.llnl.gov/search/cmip6/?activity_id=C4MIP&source_id=E3SM-1-1-ECA&experiment_id=hist-bgc>`_
* `ECA C4MIP ssp585-bgc <https://esgf-node.llnl.gov/search/cmip6/?activity_id=C4MIP&source_id=E3SM-1-1-ECA&experiment_id=ssp585-bgc>`_

Other relevant ESGF links include:
* `CTC CMIP historical <https://esgf-node.llnl.gov/search/cmip6/?activity_id=CMIP&source_id=E3SM-1-1&experiment_id=historical>`_
* `CTC ScenarioMIP ssp585 <https://esgf-node.llnl.gov/search/cmip6/?activity_id=ScenarioMIP&source_id=E3SM-1-1&experiment_id=ssp585>`_
* `CTC ScenarioMIP ssp245 <https://esgf-node.llnl.gov/search/cmip6/?activity_id=ScenarioMIP&source_id=E3SM-1-1&experiment_id=ssp245>`_
* `CTC DAMIP ​ssp245-covid <https://esgf-node.llnl.gov/search/cmip6/?activity_id=DAMIP&source_id=E3SM-1-1&experiment_id=ssp245-covid>`_
* `ECA CMIP historical <https://esgf-node.llnl.gov/search/cmip6/?activity_id=CMIP&source_id=E3SM-1-1-ECA&experiment_id=historical>`_

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   simulation_table
