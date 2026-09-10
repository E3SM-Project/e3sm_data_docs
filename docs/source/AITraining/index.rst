AI Training Datasets
====================

The E3SM project and `Allen Institute for AI (Ai2) <https://allenai.org/>`_ have developed several datasets for AI and machine learning applications. These datasets have been postprocessed for ingestion by the `ACE <https://github.com/ai2cm/ace?tab=readme-ov-file#ai2-climate-emulator>`_/`FourCastNet <https://github.com/NVlabs/FourCastNet>`_ emulator.

Dataset Details
***************

- **EAMv2**: 73-year EAMv2 simulation (F2010, perpetual 2010 forcing, repeating annual SST cycle from 2005-2014 average). 6-hourly outputs. More details see: `Duncan et al. 2024 <https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2024JH000136>`_

- **EAMv3**: 51-year EAMv3 AMIP-style simulation (1970-2020, F2010 with AMIP SSTs, constant 2010 CO2). Includes multiple ENSO cycles and global warming trend. More details see: `Wu et al. 2025 <https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JH000774>`_

- **E3SMv3**: 105-year fully coupled E3SMv3 pre-industrial control (piControl) simulation, regridded to a 180x360 grid and vertically coarsened to 8 atmosphere layers and 19 ocean depth levels. Includes 6-hourly atmosphere output and 5-day mean ocean and sea ice output. Used to train `SamudrACE <https://github.com/ai2cm/ace>`_, which couples the ACE2 atmosphere emulator with the `Samudra <https://github.com/m2lines/Samudra>`_ full-depth ocean emulator. See the `E3SM newsletter article <https://e3sm.org/a-fully-coupled-ai-emulator-of-e3smv3-reproduces-its-statistics/>`_ for an overview. More details see: `Wu et al. 2026 <https://arxiv.org/abs/2608.10277>`_

- **SCREAMv1**: Simple Cloud-Resolving E3SM Atmosphere Model version 1 training data (coming soon)

.. tip::
   Check the ``archive_contents`` text file to see files included in each tar archive. You can selectively download the files you need.

.. note::
   The EAMv2 and EAMv3 datasets are distributed as netCDF files. The E3SMv3 coupled dataset is
   distributed as `Zarr v3 <https://zarr-specs.readthedocs.io/en/latest/v3/core/index.html>`_ stores
   (using the sharding codec), which require ``zarr-python`` >= 3.0 to read. In both cases the
   vertical dimension is split across separate variables (``T_0``, ``T_1``, ...), with the vertical
   grid defined by the ``ak_*``/``bk_*`` coefficients as ``pressure = ak * P0 + bk * PS``.

Data Access
***********

.. toctree::
   :maxdepth: 2

   simulation_data/simulation_table