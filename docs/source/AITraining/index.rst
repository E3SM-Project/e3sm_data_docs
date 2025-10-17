AI Training Datasets
====================

The E3SM project and `Allen Institute for AI (Ai2) <https://allenai.org/>`_ have developed several datasets for AI and machine learning applications. These datasets have been postprocessed for ingestion by the `ACE <https://github.com/ai2cm/ace?tab=readme-ov-file#ai2-climate-emulator>`_/`FourCastNet <https://github.com/NVlabs/FourCastNet>`_ emulator.

Dataset Details
***************

- **EAMv2**: 73-year EAMv2 simulation (F2010, perpetual 2010 forcing, repeating annual SST cycle from 2005-2014 average). 6-hourly outputs. More details see: `Duncan et al. 2024 <https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2024JH000136>`_

- **EAMv3**: 51-year EAMv3 AMIP-style simulation (1970-2020, F2010 with AMIP SSTs, constant 2010 CO2). Includes multiple ENSO cycles and global warming trend. More details see: `Wu et al. 2025 <https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JH000774>`_

- **E3SMv3**: Coupled pre-industrial and historical training data (coming soon)

- **SCREAMv1**: Simple Cloud-Resolving E3SM Atmosphere Model version 1 training data (coming soon)

.. tip::
   Check the ``archive_contents`` text file to see files included in each tar archive. You can selectively download the files you need.

Data Access
***********

.. toctree::
   :maxdepth: 2

   simulation_data/simulation_table