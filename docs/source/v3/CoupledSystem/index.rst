E3SMv3 (Coupled)
================

The simulation campaign for E3SMv3 (Coupled System) was performed initially with the
**v3.LR** (lower resolution) model configuration.

If you use data from this simulation campaign, please cite the relevant overview
manuscripts.

* For a general E3SMv3 overview and v3.LR simulations:

  * Xie et al. (2025). The Energy Exascale Earth System Model Version 3. Part I: Overview of the Atmospheric Component.
  * Golaz et al. (2025). The Energy Exascale Earth System Model Version 3. Part II: Overview of the Coupled system. Submitted to JAMES.

For information on how to access and use the simulation data, see :doc:`../../v2/WaterCycle/simulation_data/index`.

**Additional tip for users without NERSC access**: If you don't have access to zstash via a NERSC account, you can first download the ``index.db`` file and use sqlite to check the archive contents before downloading specific tar files: ::

   sqlite3 index.db "SELECT tar,name,size from files;" > archive_contents.txt

This will help you identify which tar files contain the data you need before downloading.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   simulation_data/index