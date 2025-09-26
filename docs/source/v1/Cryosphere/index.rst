E3SMv1 (Cryosphere)
====================

The `E3SM version 1 cryosphere simulation campaign <https://e3sm.org/research/cryosphere-ocean/v1-cryosphere-ocean/>`_ includes standard set of 
Coupled Model Intercomparison Project Phase 6 (`CMIP6 <https://www.geosci-model-dev.net/9/1937/2016/>`_) 
Diagnosis, Evaluation, and Characterization of Klima (DECK) simulations. 
These E3SM simulations at standard resolution have been completed and the data is publicly available.

Data Resolution:

The standard resolution configuration of E3SM v1.0 cryosphere configuration has approximate horizontal resolution of 
1 deg latitude by 1 deg longitude in atmosphere (110 km grid spacing), 
with ocean and sea ice grid of 60 km in the mid-latitudes and 30 km at the equator and poles, 
and river transport at 55 km horizontal resolution. 
This model configuration is described in  
`“v1 1 deg CMIP” <https://e3sm.org/model/scientifically-validated-configurations/v1-configurations/v1-1-deg-cmip6/>`_ page 
in `Scientifically Validated Configurations <https://e3sm.org/model/scientifically-validated-configurations/>`_.

For more details, 
refer to `Coupled E3SM v1 Model Overview <https://e3sm.org/overview-paper-on-coupled-model/>`_ or to the reference papers:

* *The DOE E3SM Coupled Model Version 1: Overview and Evaluation at Standard Resolution* `doi: 10.1029/2018MS001603 <https://doi.org/10.1029/2018MS001603>`_
* *Description of historical and future projection simulations by the global coupled E3SMv1.0 model as used in CMIP6* `doi:10.5194/gmd-15-3941-2022 <https://doi.org/10.5194/gmd-15-3941-2022>`_
* *Ensemble Spread Behavior in Coupled Climate Models: Insights From the Energy Exascale Earth System Model Version 1 Large Ensemble* `doi:10.1029/2023MS003653 <https://doi.org/10.1029/2023MS003653>`_
* *The DOE E3SM Coupled Model Version 1: Description and Results at High Resolution* `doi:10.1029/2019MS001870 <https://doi.org/10.1029/2019MS001870>`_
* *The DOE E3SM v1.2 Cryosphere Configuration: Description and Simulated Antarctic Ice-Shelf Basal Melting* `doi:10.1029/2021MS002468 <https://doi.org/10.1029/2021MS002468>`_
* *Ice-shelf freshwater triggers for the Filchner–Ronne Ice Shelf melt tipping point in a global ocean–sea-ice model* `doi:10.5194/tc-18-2917-2024 <https://doi.org/10.5194/tc-18-2917-2024>`_

Experiments:

The datasets include the following experiments.

* 20190430.A_WCYCL1850-DIB-ISMF_CMIP6.ne30_oECv3wLI.control.cori-knl -- 1850 piControl with standard snowcapping, constant GM (200 years)
* 20190306.A_WCYCL1850-DIB-ISMF_CMIP6.ne30_oECv3wLI.edison -- 1850 piControl with ice shelf melt fluxes, constant GM (200 years)
* 20210614.A_WCYCL1850-DIB-ISMF_CMIP6.ne30_oECv3wLI.DIBbugfix.anvil -- 1850 piControl with ice shelf melt fluxes, constant GM (200 years), bug fix run
* 20200610.A_WCYCL1850-DIB-ISMF_CMIP6.ne30_ECwISC30to60E1r2.cori-knl.maint1p2-3DGM -- 1850 piControl with ice shelf melt fluxes, variable GM (200 years)
* 20210614.A_WCYCL1850-DIB-ISMF_CMIP6.ne30_ECwISC30to60E1r2.anvil.DIBbugFixMGM -- 1850 piControl with ice shelf melt fluxes, variable GM (200 years), bug fix run
* 20190923.GMPAS-IAF.T62_oEC60to30v3wLI.cori-knl -- Ocean-Ice only (CORE-II atmosphere forced), constant GM, uniform iceberg spreading (100 years)
* 20190225.GMPAS-DIB-IAF-ISMF.T62_oEC60to30v3wLI.cori-knl -- Ocean-Ice only (CORE-II atmosphere forced), constant GM, data iceberg spreading (210 years)
* 20190819.GMPAS-DIB-IAF-ISMF.T62_oEC60to30v3wLI.cori-knl.testNewGM -- Ocean-Ice only (CORE-II atmosphere forced), variable GM, data iceberg spreading (210 years)


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   simulation_data/index
