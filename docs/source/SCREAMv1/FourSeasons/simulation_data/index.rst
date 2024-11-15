***************
Simulation Data 
***************

The SCREAMv1 FourSeasons simulation data is available on **NERSC HPSS**.

**If you have an account on NERSC**, you can retrieve the data locally or remotely using Globus.

To download simulation data locally on a NERSC machine: ::

   zstash extract --hpss=<HPSS path below>

To download simulation data remotely using the zstash Globus interface: ::

   zstash extract --hpss=globus://nersc/<HPSS path below>

or ::

   zstash extract --hpss=globus://9cd89cfd-6d04-11e5-ba46-22000b92c6ec/<HPSS path below>

Note that the data management tool `zstash <https://github.com/E3SM-Project/zstash>`_ is available from the `E3SM-Unified <https://github.com/E3SM-Project/e3sm-unified>`_ conda environment. 

For more information, refer to `zstash usage <https://e3sm-project.github.io/zstash/_build/html/master/usage.html#extract>`_. 

**If you do not have access to NERSC**, you can download simulation data directly through the  NERSC HPSS
`web interface <https://portal.nersc.gov/archive/home/a/adonahue/www/>`_.
Note that this will be slow and inefficient since you'll have to download the individual files.


Original Run Scripts
*********************

Scripts originally used to run SCREAMv1 FourSeasons simulations are available `here <https://github.com/E3SM-Project/e3sm_data_docs/tree/main/run_scripts/SCREAMv1/original/>`_.

**Warning, these will not run out-of-the-box**.  They are provided to give guidance for setting up a similar run.

Table of simulation data
************************

.. toctree::
   :maxdepth: 2

   simulation_table
