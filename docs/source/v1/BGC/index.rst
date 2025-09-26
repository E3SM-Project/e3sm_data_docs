E3SMv1 (BGC)
====================

The `E3SM version 1 BGC simulation campaign <https://e3sm.org/research/bgc-and-energy/v1-bgc-and-energy/>`_ includes standard set of 
Coupled Model Intercomparison Project Phase 6 (`CMIP6 <https://www.geosci-model-dev.net/9/1937/2016/>`_) 
Diagnosis, Evaluation, and Characterization of Klima (DECK) simulations. 
These E3SM simulations at standard resolution have been completed and the data is publicly available.

Data Resolution:

The standard resolution configuration of E3SM v1.0 BGC configuration has approximate horizontal resolution of 
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
* (TODO: add BGC-specific papers)

Experiments:

The datasets include the following experiments. Each case has a historical run and a ssp85 run.

(TODO: add description to the top-level bullet points below)

* CTC Control

  * E3SM_1_1_piControl (20181217.CNTL_CNPCTC1850_OIBGC.ne30_oECv3.edison)
  * E3SM_1_1_piControl-ext85yr (20191204.CNTL_CNPCTC1850_OIBGC.ne30_oECv3.compy)

* CTC BCRC

  * E3SM_1_1_hist-BCRC (20181217.BCRC_CNPCTC20TR_OIBGC.ne30_oECv3.edison)
  * E3SM_1_1_ssp585-BCRC (20191107.BCRC_CNPCTC_SSP585_OIBGC.ne30_oECv3.compy)

* CTC BCRD

  * E3SM_1_1_hist-BCRD (20181217.BCRD_CNPCTC20TR_OIBGC.ne30_oECv3.edison)
  * E3SM_1_1_ssp585-BCRD (20191204.BCRD_CNPCTC_SSP585_OIBGC.ne30_oECv3.compy, 20190812.BCRD_CNPCTC20TR_OIBGC.ne30_oECv3.compy/archive)

* CTC BDRC

  * E3SM_1_1_hist-BDRC (20181217.BDRC_CNPCTC20TR_OIBGC.ne30_oECv3.edison)
  * E3SM_1_1_ssp585-BDRC (20191107.BDRC_CNPCTC_SSP585_OIBGC.ne30_oECv3.compy)

* CTC BDRD

  * E3SM_1_1_hist-BDRD (20181217.BDRD_CNPCTC20TR_OIBGC.ne30_oECv3.edison)
  * E3SM_1_1_ssp585-BDRD (20191204.BDRD_CNPCTC_SSP585_OIBGC.ne30_oECv3.compy)

* ECA Control

  * E3SM_1_1_ECA_piControl (20190308.CNTL.1850-2014)
  * E3SM_1_1_ECA_piControl-ext85yr (CNTL_CNPECACNT_SSP85.ne30_oECv3.cori-knl)

* ECA BCRC

  * E3SM_1_1_ECA_hist-BCRC (BCRC_CNPECACNT_20TR.ne30_oECv3.edison, BCRC_CNPECACNT_20TR.ne30_oECv3.cori-knl)
  * E3SM_1_1_ECA_ssp585-BCRC (BCRC_CNPECACNT_SSP85.ne30_oECv3.cori-knl)

* ECA BCRD

  * E3SM_1_1_ECA_hist-BCRD (BCRD_CNPECACNT_20TR.ne30_oECv3.edison, BCRD_CNPECACNT_20TR.ne30_oECv3.cori-knl)
  * E3SM_1_1_ECA_ssp585-BCRD (BCRD_CNPECACNT_SSP85.ne30_oECv3.cori-knl)

* ECA BDRC

  * E3SM_1_1_ECA_hist-BDRC (20190308.BDRC.1850-2014)
  * E3SM_1_1_ECA_ssp585-BDRC (20191108.BDRC.SSP85)

* ECA BDRD

  * E3SM_1_1_ECA_hist-BDRD (20190308.BDRD.1850-2014)
  * E3SM_1_1_ECA_ssp585-BDRD (20191108.BDRD.SSP85)


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   simulation_data/index
