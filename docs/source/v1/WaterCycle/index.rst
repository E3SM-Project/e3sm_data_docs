E3SMv1 (Water Cycle)
====================

The `E3SM version 1 water cycle simulation campaign <https://e3sm.org/research/water-cycle/v1-water-cycle/>`_ includes standard set of 
Coupled Model Intercomparison Project Phase 6 (`CMIP6 <https://www.geosci-model-dev.net/9/1937/2016/>`_) 
Diagnosis, Evaluation, and Characterization of Klima (DECK) simulations. 
These E3SM simulations at standard resolution have been completed and the data is publicly available.

Data Resolution:

The standard resolution configuration of E3SM v1.0 water cycle configuration has approximate horizontal resolution of 
1 deg latitude by 1 deg longitude in atmosphere (110 km grid spacing), 
with ocean and sea ice grid of 60 km in the mid-latitudes and 30 km at the equator and poles, 
and river transport at 55 km horizontal resolution. 
This model configuration is described in  
`“v1 1 deg CMIP” <https://e3sm.org/model/scientifically-validated-configurations/v1-configurations/v1-1-deg-cmip6/?preview=true>`_ page 
in `Scientifically Validated Configurations <https://e3sm.org/model/scientifically-validated-configurations/>`_.

Reference Paper:

For more details, 
refer to `Coupled E3SM v1 Model Overview <https://e3sm.org/?p=5470>`_ or 
directly to the scientific paper (`doi:10.1029/2018MS001603 <https://doi.org/10.1029/2018MS001603>`_), 
which documents the E3SM model version 1, 
its almost 3000 years of DECK simulations and discusses the model’s performance.

Experiments:

The datasets include the following experiments:

* piControl – Pre-industrial control (piControl) simulation (500 years)
* historical – Historical simulations 1850-2014 (165 years) 5 ensembles
* 1pctCO2 – Prescribed 1% / year CO2 increase (1pctCO2) simulation (150 years)
* abrupt-4xCO2 – Abrupt CO2 quadrupling (abrupt-4xCO2) simulation (150 years)
* abrupt-4xCO2-ext300yrs – Abrupt CO2 quadrupling (abrupt-4xCO2) simulation (140-300 years)
* amip – atmosphere only AMIP simulation 1870-2014 (145 years) 3 ensembles
* amip_1850_allF – atmosphere only AMIP with all forcings held at 1850 values,  1870-2014 (145 years) 3 ensembles
* amip_1850_aeroF – atmosphere only AMIP with all aerosol forcings held at 1850 values,  1870-2014 (145 years) 3 ensembles

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   simulation_data/index
   reproducing_simulations/index