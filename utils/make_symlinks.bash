# # This will be a problem if these simulations are ever removed from the publication archives!
# for i in $(seq 1 20); do
#     hsi ln -s /home/projects/e3sm/www/publication-archives/pub_archive_E3SM_1_0_LE_historical_ens$i /home/projects/e3sm/www/WaterCycle/E3SMv1/LR/LE_historical_ens$i
# done

# for i in $(seq 1 20); do
#     hsi ln -s /home/projects/e3sm/www/publication-archives/pub_archive_E3SM_1_0_LE_ssp370_ens$i /home/projects/e3sm/www/WaterCycle/E3SMv1/LR/LE_ssp370_ens$i
# done

# # Symlink last remaining large simulation
# # This will be a problem if ndk ever deletes the source!
# hsi ln -s /home/n/ndk/2019/theta.20190910.branch_noCNT.n825def.unc06.A_WCYCL1950S_CMIP6_HR.ne120_oRRS18v3_ICG /home/projects/e3sm/www/WaterCycle/E3SMv1/LR/theta.20190910.branch_noCNT.n825def.unc06.A_WCYCL1950S_CMIP6_HR.ne120_oRRS18v3_ICG

# Note:
# It seems impossible to do a recursive remove with HSI/on HPSS.
# > rm -rf E3SM_1_0_LE_historical_ens1@ # Trying to remove mislabeled directory
# Unknown option or missing argument: 'r' ignored
# Unknown option or missing argument: 'f' ignored

### Cryosphere ###
# hsi ln -s /home/d/dcomeau/cryosphere_simulations/20190430.A_WCYCL1850-DIB-ISMF_CMIP6.ne30_oECv3wLI.control.cori-knl /home/projects/e3sm/www/Cryosphere/E3SMv1/20190430.A_WCYCL1850-DIB-ISMF_CMIP6.ne30_oECv3wLI.control.cori-knl
# for simulation in "20190306.A_WCYCL1850-DIB-ISMF_CMIP6.ne30_oECv3wLI.edison" "20190923.GMPAS-IAF.T62_oEC60to30v3wLI.cori-knl" "20190225.GMPAS-DIB-IAF-ISMF.T62_oEC60to30v3wLI.cori-knl" "20200610.A_WCYCL1850-DIB-ISMF_CMIP6.ne30_ECwISC30to60E1r2.cori-knl.maint1p2-3DGM" "20190819.GMPAS-DIB-IAF-ISMF.T62_oEC60to30v3wLI.cori-knl.testNewGM" "20210614.A_WCYCL1850-DIB-ISMF_CMIP6.ne30_oECv3wLI.DIBbugfix.anvil" "20210614.A_WCYCL1850-DIB-ISMF_CMIP6.ne30_ECwISC30to60E1r2.anvil.DIBbugFixMGM"; do
#     hsi ln -s /home/projects/m3412/${simulation} /home/projects/e3sm/www/Cryosphere/E3SMv1/${simulation}
# done

### BGC ###
# https://e3sm.atlassian.net/wiki/spaces/ED/pages/4495441922/V1+Simulation+backfill+WIP
# We'll use symlinks to the publication archives
declare -A simulation_map=(
    # CTC Control
    ["20181217.CNTL_CNPCTC1850_OIBGC.ne30_oECv3.edison"]="pub_archive_E3SM_1_1_piControl"
    ["20191204.CNTL_CNPCTC1850_OIBGC.ne30_oECv3.compy"]="pub_archive_E3SM_1_1_piControl-ext85yr"
    # CTC BCRC
    ["20181217.BCRC_CNPCTC20TR_OIBGC.ne30_oECv3.edison"]="pub_archive_E3SM_1_1_hist-BCRC"
    ["20191107.BCRC_CNPCTC_SSP585_OIBGC.ne30_oECv3.compy"]="pub_archive_E3SM_1_1_ssp585-BCRC"
    # CTC BCRD
    ["20181217.BCRD_CNPCTC20TR_OIBGC.ne30_oECv3.edison"]="pub_archive_E3SM_1_1_hist-BCRD"
    # These 2 map to the same pub archive:
    ["20191204.BCRD_CNPCTC_SSP585_OIBGC.ne30_oECv3.compy"]="pub_archive_E3SM_1_1_ssp585-BCRD"
    ["20190812.BCRD_CNPCTC20TR_OIBGC.ne30_oECv3.compy/archive"]="pub_archive_E3SM_1_1_ssp585-BCRD"
    # CTC BDRC
    ["20181217.BDRC_CNPCTC20TR_OIBGC.ne30_oECv3.edison"]="pub_archive_E3SM_1_1_hist-BDRC"
    ["20191107.BDRC_CNPCTC_SSP585_OIBGC.ne30_oECv3.compy"]="pub_archive_E3SM_1_1_ssp585-BDRC"
    # CTC BDRD
    ["20181217.BDRD_CNPCTC20TR_OIBGC.ne30_oECv3.edison"]="pub_archive_E3SM_1_1_hist-BDRD"
    ["20191204.BDRD_CNPCTC_SSP585_OIBGC.ne30_oECv3.compy"]="pub_archive_E3SM_1_1_ssp585-BDRD"
    # ECA Control
    ["20190308.CNTL.1850-2014"]="pub_archive_E3SM_1_1_ECA_piControl"
    ["CNTL_CNPECACNT_SSP85.ne30_oECv3.cori-knl"]="pub_archive_E3SM_1_1_ECA_piControl-ext85yr"
    # ECA BCRC
    # These 2 map to the same pub archive:
    ["BCRC_CNPECACNT_20TR.ne30_oECv3.edison"]="pub_archive_E3SM_1_1_ECA_hist-BCRC"
    ["BCRC_CNPECACNT_20TR.ne30_oECv3.cori-knl"]="pub_archive_E3SM_1_1_ECA_hist-BCRC"
    ["BCRC_CNPECACNT_SSP85.ne30_oECv3.cori-knl"]="pub_archive_E3SM_1_1_ECA_ssp585-BCRC"
    # ECA BCRD
    # These 2 map to the same pub archive:
    ["BCRD_CNPECACNT_20TR.ne30_oECv3.edison"]="pub_archive_E3SM_1_1_ECA_hist-BCRD"
    ["BCRD_CNPECACNT_20TR.ne30_oECv3.cori-knl"]="pub_archive_E3SM_1_1_ECA_hist-BCRD"
    ["BCRD_CNPECACNT_SSP85.ne30_oECv3.cori-knl"]="pub_archive_E3SM_1_1_ECA_ssp585-BCRD"
    # ECA BDRC
    ["20190308.BDRC.1850-2014"]="pub_archive_E3SM_1_1_ECA_hist-BDRC"
    ["20191108.BDRC.SSP85"]="pub_archive_E3SM_1_1_ECA_ssp585-BDRC"
    # ECA BDRD
    ["20190308.BDRD.1850-2014"]="pub_archive_E3SM_1_1_ECA_hist-BDRD"
    ["20191108.BDRD.SSP85"]="pub_archive_E3SM_1_1_ECA_ssp585-BDRD"
)
keys=("${!simulation_map[@]}")
for key in "${keys[@]}"; do
    echo "$key = ${simulation_map[$key]}"
done
pub_archive=/home/projects/e3sm/www/publication-archives
centralized_dir=/home/projects/e3sm/www/BGC/E3SMv1
echo "Create symlinks from ${pub_archive} to ${centralized_dir}:"
for key in "${keys[@]}"; do
    original_simulation_name=$key
    pub_archive_name=${simulation_map[$key]}
    echo "Would run: hsi ln -s ${pub_archive}/${pub_archive_name} ${centralized_dir}/${original_simulation_name}"
done