# v1 BGC
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
original_name_list=("${!simulation_map[@]}")
echo "Experiments:"
echo ""
echo "The datasets include the following experiments."
echo ""
for original_name in "${original_name_list[@]}"; do
    display_name_with_prefix=${simulation_map[${original_name}]}
    display_name="${display_name_with_prefix#pub_archive_}"
    echo "* ${display_name} (${original_name})"
done

# NOTE: You will have to manually remove repeats of the same display_name
# (i.e.,) cases where two original directories map to the same pub archive