# Available data

As new data is added to either E3SM Data Docs or the ESGF node, the table below should be updated. 

Relevant links:
- [ESGF Nodes](https://esgf.github.io/nodes.html)
- [ESGF NERSC Node search](https://metagrid.esgf-west.org/search)
- [ESGF ORNL Node search](https://esgf-node.ornl.gov/search)

## ESGF NERSC Node Search

[ESGF NERSC Node search](https://metagrid.esgf-west.org/search) results (as of 2026-08-06)

The first 5 columns refer to information on ESGF. The last 3 columns refer to information on E3SM Data Docs. If the last 3 columns are empty, that means this data on ESGF is _not_ documented on E3SM Data Docs. 

| Project | Identifiers > Institution ID | Identifiers > Source ID | General > Activity ID | Identifiers > Experiment ID | Relevant simulation table | Relevant rows | ESGF links |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CMIP6 | E3SM-Project (17,846) | E3SM-1-0 (3,084) | CMIP (1936)| 1pctCO2 (190) | [v1 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v1/WaterCycle/simulation_data/simulation_table.html) | LR> DECK, 1 row | No |
| | | | | abrupt-4xCO2 (193) | [v1 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v1/WaterCycle/simulation_data/simulation_table.html) | LR > DECK, 2 rows | 1 out of 2 (CMIP only) |
| | | | | amip (407) | [v1 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v1/WaterCycle/simulation_data/simulation_table.html) | LR > AMIP, 9 rows | 3 out of 9 (CMIP only) |
| | | | | historical (965) | [v1 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v1/WaterCycle/simulation_data/simulation_table.html) | LR > Historical, 5 rows | Yes (CMIP only) |
| | | | | piControl (181) | [v1 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v1/WaterCycle/simulation_data/simulation_table.html) | LR> DECK, 1 row | Yes (CMIP only) |
| | | | DAMIP (381) | hist-GHG (381) | [v1 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v1/WaterCycle/simulation_data/simulation_table.html) | LR > DAMIP, 3 rows | No |
| | | | ScenarioMIP (767) | ssp585 (767) | [v1 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v1/WaterCycle/simulation_data/simulation_table.html) | LR > Projection, 8 rows | No |
| | | E3SM-1-1 (1,750) | C4MIP (333) | hist-bgc (172) | [v1 BGC](https://docs.e3sm.org/e3sm_data_docs/_build/html/v1/BGC/simulation_data/simulation_table.html) | LR > CTC ... 4 rows include "hist" | No |
| | | | | ssp585-bgc (161) | [v1 BGC](https://docs.e3sm.org/e3sm_data_docs/_build/html/v1/BGC/simulation_data/simulation_table.html) | LR > CTC ... 4 rows include "ssp585" | No |
| | | | CMIP (392) | historical (195) | | | |
| | | | | piControl (197) | | | |
| | | | DAMIP (540) | ssp245-covid (540) | | | |
| | | | ScenarioMIP (485) | ssp245 (322) | | | |
| | | | | ssp585 (163) | | | |
| | | E3SM-1-1-ECA (927) | C4MIP (332) | hist-bgc (171) | [v1 BGC](https://docs.e3sm.org/e3sm_data_docs/_build/html/v1/BGC/simulation_data/simulation_table.html) | LR > ECA ... 4 rows include "hist" | No |
| | | | | ssp585-bgc (161) | [v1 BGC](https://docs.e3sm.org/e3sm_data_docs/_build/html/v1/BGC/simulation_data/simulation_table.html) | LR > ECA ... 4 rows include "ssp585" | No |
| | | | CMIP (426) | historical (215) | | | |
| | | | | piControl (211) | | | |
| | | | ScenarioMIP (169) | ssp585 (169) | | | |
| | | E3SM-2-0 (8,589; see ERROR note) | AerChemMIP (2,583) | piClim-control (77) | | | |
| | | | | ssp370 (2,506) | | | |
| | | | CMIP (3,687) | 1pctCO2 (152) | [v2 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2/WaterCycle/simulation_data/simulation_table.html) | LR > DECK, 1 row | Yes (CMIP, Native) |
| | | | | abrupt-4xCO2 (271) | [v2 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2/WaterCycle/simulation_data/simulation_table.html) | LR > DECK, 2 rows | Yes (CMIP, Native) |
| | | | | amip (286) | [v2 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2/WaterCycle/simulation_data/simulation_table.html) | LR > AMIP, 4 rows | 3 out of 4 (CMIP, Native) |
| | | | | historical (2,814) | [v2 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2/WaterCycle/simulation_data/simulation_table.html) | LR > Historical, 6 rows | 5 out of 6 (CMIP, Native) |
| | | | | piControl (164) | [v2 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2/WaterCycle/simulation_data/simulation_table.html) | LR > DECK, 2 rows | 1 out of 2 (CMIP, Native) |
| | | | DAMIP (1,857) | hist-aer (619) | [v2 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2/WaterCycle/simulation_data/simulation_table.html) | LR > Single-Forcing (DAMIP-like), 5 rows | 5 out of 5 (CMIP, Native) |
| | | | | hist-GHG (619) | [v2 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2/WaterCycle/simulation_data/simulation_table.html) | LR > Single-Forcing (DAMIP-like), 5 rows | 5 out of 5 (CMIP, Native) |
| | | | | hist-nat (619) |[v2 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2/WaterCycle/simulation_data/simulation_table.html) | LR > Single-Forcing (DAMIP-like), 5 rows (labeled "all-xGHG-xaer") | 5 out of 5 (CMIP, Native) |
| | | | RFMIP (539) | piClim-control (77) | [v2 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2/WaterCycle/simulation_data/simulation_table.html) | LR > RFMIP, 1 row | Yes (CMIP, Native) |
| | | | | piClim-histaer (231) | [v2 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2/WaterCycle/simulation_data/simulation_table.html) | LR > RFMIP, 3 rows | Yes (CMIP, Native) |
| | | | | piClim-histall (231) | [v2 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2/WaterCycle/simulation_data/simulation_table.html) | LR > RFMIP, 3 rows | Yes (CMIP, Native) |
| | | | ScenarioMIP (2,506) | ssp370 (2,506) | | | |
| | | E3SM-2-0-NARRM (1,502) | CMIP (1,502) | 1pctCO2 (152) |  [v2 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2/WaterCycle/simulation_data/simulation_table.html) | NARRM > DECK, 1 row | Yes (CMIP, Native) |
| | | | | abrupt-4xCO2 (152) |  [v2 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2/WaterCycle/simulation_data/simulation_table.html) | NARRM > DECK, 1 row | Yes (CMIP, Native) |
| | | | | amip (286) | [v2 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2/WaterCycle/simulation_data/simulation_table.html) | NARRM > AMIP, 4 rows | 3 out of 4 (CMIP, Native) |
| | | | | historical (748) | [v2 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2/WaterCycle/simulation_data/simulation_table.html) | NARRM > Historical, 6 rows | 5 out of 6 (CMIP, Native) |
| | | | | piControl (164) | [v2 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2/WaterCycle/simulation_data/simulation_table.html) | NARRM > DECK, 1 row | Yes (CMIP, Native) |
| | | E3SM-2-1 (1,994) | CMIP (1,994) | 1pctCO2 (230) | [v2.1 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2.1/WaterCycle/simulation_data/simulation_table.html)| LR > DECK, 1 row | Yes (CMIP only) |
| | | | | abrupt-4xCO2 (230) | [v2.1 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2.1/WaterCycle/simulation_data/simulation_table.html) | LR > DECK, 1 row | Yes (CMIP only) |
| | | | | amip (154) | [v2.1 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2.1/WaterCycle/simulation_data/simulation_table.html)| LR > DECK, 1 row | Yes (CMIP only) |
| | | | | historical (1,150) | [v2.1 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2.1/WaterCycle/simulation_data/simulation_table.html)| LR > Historical, 5 rows | Yes (CMIP only) |
| | | | | piControl (230) | [v2.1 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2.1/WaterCycle/simulation_data/simulation_table.html)| LR > DECK, 1 row | Yes (CMIP only) |
| CMIP6-E3SM-Ext | E3SM-Project (16,982) | E3SM-3-0 (16,982) | CMIP (7,222) | 1pctCO2 (230) | [v3 CoupledSystem](https://docs.e3sm.org/e3sm_data_docs/_build/html/v3/CoupledSystem/simulation_data/simulation_table.html) | LR > DECK, 1 row | Yes (CMIP only) |
| | | | | abrupt-4xCO2 (228) | [v3 CoupledSystem](https://docs.e3sm.org/e3sm_data_docs/_build/html/v3/CoupledSystem/simulation_data/simulation_table.html) | LR > DECK, 1 row | Yes (CMIP only) |
| | | | | amip (462) | [v3 CoupledSystem](https://docs.e3sm.org/e3sm_data_docs/_build/html/v3/CoupledSystem/simulation_data/simulation_table.html) | LR > AMIP, 3 rows | Yes (CMIP only) |
| | | | | historical (6,072) | [v3 CoupledSystem](https://docs.e3sm.org/e3sm_data_docs/_build/html/v3/CoupledSystem/simulation_data/simulation_table.html) | LR > Historical, 5 rows | Yes (CMIP only) |
| | | | | piControl (230) | [v3 CoupledSystem](https://docs.e3sm.org/e3sm_data_docs/_build/html/v3/CoupledSystem/simulation_data/simulation_table.html) | LR > DECK, 1 row | Yes (CMIP only) |
| | | | DAMIP (2,070) | hist-aer (690) | [v3 CoupledSystem](https://docs.e3sm.org/e3sm_data_docs/_build/html/v3/CoupledSystem/simulation_data/simulation_table.html) | LR > Single-Forcing (DAMIP-like), 3 rows | Yes (CMIP only) |
| | | | | hist-GHG (690) | [v3 CoupledSystem](https://docs.e3sm.org/e3sm_data_docs/_build/html/v3/CoupledSystem/simulation_data/simulation_table.html) | LR > Single-Forcing (DAMIP-like), 3 rows | Yes (CMIP only) |
| | | | | hist-nat (690) | [v3 CoupledSystem](https://docs.e3sm.org/e3sm_data_docs/_build/html/v3/CoupledSystem/simulation_data/simulation_table.html) | LR > Single-Forcing (DAMIP-like), 3 rows | Yes (CMIP only) |
| | | | RFMIP (1,540) | piClim-control (154) | [v3 CoupledSystem](https://docs.e3sm.org/e3sm_data_docs/_build/html/v3/CoupledSystem/simulation_data/simulation_table.html) | LR > RFMIP, 1 row | Yes (CMIP only) |
| | | | | piClim-histaer (462) | [v3 CoupledSystem](https://docs.e3sm.org/e3sm_data_docs/_build/html/v3/CoupledSystem/simulation_data/simulation_table.html) | LR > RFMIP, 3 rows | Yes (CMIP only) |
| | | | | piClim-histall (462) | [v3 CoupledSystem](https://docs.e3sm.org/e3sm_data_docs/_build/html/v3/CoupledSystem/simulation_data/simulation_table.html) | LR > RFMIP, 3 rows | Yes (CMIP only) |
| | | | | piClim-histghg (462) | [v3 CoupledSystem](https://docs.e3sm.org/e3sm_data_docs/_build/html/v3/CoupledSystem/simulation_data/simulation_table.html) | LR > RFMIP, 3 rows | Yes (CMIP only) |
| | | | ScenarioMIP (6,150) | ssp245 (6,150) | | | |

ERROR: 8,589 does not equal sum of Activity ID counts (11,172). It's off by 2,583; perhaps the search feature is not counting AerChemMIP? 

### How to fill out the above table

1. Go to the search link
2. Manually drill down through the facet search menu. The full list of options for each facet will only appear if you keep your mouse there, so it is more convenient to screenshot the full list and then manually copy over the data to the table above.
3. Go through the simulation tables on E3SM Data Docs and fill in the relevant data.

### Simulations included on E3SM Data Docs but NOT on ESGF

E3SM Data Docs simulation tables with no data on ESGF:
- [v1 Cyrosphere](https://docs.e3sm.org/e3sm_data_docs/_build/html/v1/Cryosphere/simulation_data/simulation_table.html)
- [v2.1 BGC](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2.1/BGC/simulation_data/simulation_table.html)
- [SCREAMv0 DYAMOND2](https://docs.e3sm.org/e3sm_data_docs/_build/html/SCREAMv0/DYAMOND2/simulation_data/simulation_table.html)
- [SCREAMv1 Four-Seasons](https://docs.e3sm.org/e3sm_data_docs/_build/html/SCREAMv1/FourSeasons/simulation_data/simulation_table.html)
- [AI Training Datasets](https://docs.e3sm.org/e3sm_data_docs/_build/html/AITraining/simulation_data/simulation_table.html)

E3SM Data Docs simulation tables with rows not accounted for on ESGF:
- [v1 BGC](https://docs.e3sm.org/e3sm_data_docs/_build/html/v1/BGC/simulation_data/simulation_table.html): LR > CTC Control, LR > ECA Control
- [v1 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v1/WaterCycle/simulation_data/simulation_table.html): LR > LargeEnsemble (these have CMIP ESGF links), all HR rows
- [v2 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2/WaterCycle/simulation_data/simulation_table.html): LR > Historical LE (these have CMIP ESGF links), LR > Other, NARRM > Other

For reference, E3SM Data Docs simulation tables with _all_ rows accounted for on ESGF:
- [v2.1 WaterCycle](https://docs.e3sm.org/e3sm_data_docs/_build/html/v2.1/WaterCycle/simulation_data/simulation_table.html)
- [v3 CoupledSystem](https://docs.e3sm.org/e3sm_data_docs/_build/html/v3/CoupledSystem/simulation_data/simulation_table.html)

### Combined summary

| Source ID | On ESGF, but missing on Data Docs | On Data Docs, but missing on ESGF |
| --- | --- | --- |
| E3SM-1-0 | None | v1 Cyrosphere, v1 WaterCycle (specifically LR > LargeEnsemble (but these actually have CMIP ESGF links), all HR rows) |
| E3SM-1-1 | CMIP, DAMIP, ScenarioMIP | v1 BGC (specifically LR > CTC Control) |
| E3SM-1-1-ECA | CMIP, ScenarioMIP | v1 BGC (specifically LR > ECA Control) |
| E3SM-2-0 | AerChemMIP, ScenarioMIP | v2 WaterCycle (specifically LR > Historical LE (but these actually have CMIP ESGF links), LR > Other) |
| E3SM-2-0-NARRM | None | v2 WaterCycle (specifically NARRM > Other) |
| E3SM-2-1 | None | v2.1 BGC |
| E3SM-3-0 | ScenarioMIP | None |
| N/A | N/A | SCREAMv0 DYAMOND2, SCREAMv1 Four-Seasons, AI Training Datasets


## ESGF ORNL Node Search

[ESGF ORNL Node search](https://esgf-node.ornl.gov/search) results (as of 2026-08-06)

| Project | Identifiers > Institution ID | Notes |
| --- | --- | --- |
| CMIP6 | E3SM-Project (17,846) | Results appear identical to NERSC node search |
| E3SM | N/A | 16,982 results found |
