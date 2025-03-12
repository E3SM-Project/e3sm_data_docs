#!/bin/bash -fe

# CBGCv2-LNDATM transient run script for Chyrsalis
# 

main() {

# For debugging, uncomment libe below
#set -x

# --- Configuration flags ----

# Machine and project
readonly MACHINE=chrysalis
readonly PROJECT="e3sm"

# Simulation
readonly MYDATE=$(date '+%Y%m%d')
# readonly MYDATE="test"
readonly COMPSET="BGCEXP_LNDATM_CNPRDCTC_20TR"
readonly RESOLUTION="ne30pg2_r05_EC30to60E2r2"
readonly CASE_NAME="v2.LR.BGC-LNDATM.CONTRL"
readonly CASE_GROUP="v2.LR.LNDATMcontrol"

# Code and compilation
#readonly CHECKOUT="${MYDATE}"
readonly BRANCH="main" # sfeng/lnd/lnd-atm-20tr merged to main on 10/13/2022
#$(git rev-parse HEAD) #"9f0094d40f039769ba68ed4e89810516838ad43f"
#readonly CHERRY=( "7e4d1c9fec40ce1cf2c272d671f5d9111fa4dea7" "a5b1d42d7cd24924d0dbda95e24ad8d4556d93f1" ) # PR4349
readonly DEBUG_COMPILE=false

# Run options
readonly MODEL_START_TYPE="hybrid"  # 'initial', 'continue', 'branch', 'hybrid'
readonly START_DATE="1850-01-01"

# Additional options for 'branch' and 'hybrid'
readonly GET_REFCASE=TRUE
# will need to change the following variables according to initial files
readonly RUN_REFDIR="/lcrc/group/e3sm/ac.sfeng1/E3SM_Simulations/20221109.v2.LR.BGC-LNDATM.SPINUP.ne30pg2_r05_EC30to60E2r2.chrysalis/archive/rest/0501-01-01-00000"
readonly RUN_REFCASE="v2.LR.BGC-LNDATM.SPINUP" 
readonly RUN_REFDATE="0501-01-01"   # same as MODEL_START_DATE for 'branch', can be different for 'hybrid'

# Set paths
readonly CODE_ROOT="${HOME}/code/E3SMv2.1/E3SM"
readonly CASE_ROOT="/lcrc/group/e3sm2/ac.sfeng1/E3SM_Simulations/${MYDATE}.${CASE_NAME}.${RESOLUTION}.${MACHINE}"

# Sub-directories
readonly CASE_BUILD_DIR=${CASE_ROOT}/build
readonly CASE_ARCHIVE_DIR=${CASE_ROOT}/archive

# Define type of run
#  short tests: 'XS_2x5_ndays', 'XS_1x10_ndays', 'S_1x10_ndays', 
#               'M_1x10_ndays', 'M2_1x10_ndays', 'M80_1x10_ndays', 'L_1x10_ndays'
#  or 'production' for full simulation
readonly run='production'
#readonly run='XL_12x2_nmonths'
#readonly run='L_12x2_nmonths'
# readonly run='S_12x2_nmonths'
if [ "${run}" != "production" ]; then

  # Short test simulations
  tmp=($(echo $run | tr "_" " "))
  layout=${tmp[0]}
  units=${tmp[2]}
  resubmit=$(( ${tmp[1]%%x*} -1 ))
  length=${tmp[1]##*x}
   
  readonly CASE_SCRIPTS_DIR=${CASE_ROOT}/tests/${run}/case_scripts
  readonly CASE_RUN_DIR=${CASE_ROOT}/tests/${run}/run
  readonly PELAYOUT=${layout}
  readonly STOP_OPTION=${units}
  readonly STOP_N=${length}
  readonly REST_OPTION=${STOP_OPTION}
  readonly REST_N=${STOP_N}
  readonly RESUBMIT=${resubmit}
  readonly DO_SHORT_TERM_ARCHIVING=false
  
  if [ "${layout}" = "XS" ] | [ "${layout}" = "S" ]; then
     readonly WALLTIME="0:30:00"
     readonly IFDEBUG="debug"
  else
    readonly WALLTIME="4:00:00"
    readonly IFDEBUG="debug"
  fi  

else

  # Production simulation
  readonly CASE_SCRIPTS_DIR=${CASE_ROOT}/case_scripts
  readonly CASE_RUN_DIR=${CASE_ROOT}/run
  readonly PELAYOUT="XL"
#   readonly WALLTIME="24:00:00"
#   readonly STOP_OPTION="nyears"
#   readonly STOP_N="40"
#   readonly REST_OPTION="nyears"
#   readonly REST_N="5"
#   readonly RESUBMIT="5"
#   readonly DO_SHORT_TERM_ARCHIVING=false
#   readonly IFDEBUG="compute"
  readonly WALLTIME="132:00:00"
  readonly STOP_OPTION="nyears"
  readonly STOP_N="165"
  readonly REST_OPTION="nyears"
  readonly REST_N="5"
  readonly RESUBMIT="0"
  readonly DO_SHORT_TERM_ARCHIVING=false
  readonly IFDEBUG="compute"
fi

# Coupler history 
readonly HIST_OPTION="nyears"
readonly HIST_N="5"

# Leave empty (unless you understand what it does)
readonly OLD_EXECUTABLE=""

# --- Toggle flags for what to do ----
do_fetch_code=false
do_create_newcase=true
do_modify_pe_layout=true
do_case_setup=true
do_case_build=true
do_case_submit=true

# --- Now, do the work ---

# Make directories created by this script world-readable
umask 022

# Fetch code from Github
fetch_code

# Create case
create_newcase

#change PE layout
modify_pe_layout

# Setup
case_setup

# Build
case_build

# Configure runtime options
runtime_options

# Copy script into case_script directory for provenance
copy_script

# Submit
case_submit

# All done
echo $'\n----- All done -----\n'

# # set prority 
# scontrol update account=priority partition=priority JobId=######

}

# =======================
# Custom user_nl settings
# =======================

user_nl() {

cat << EOF >> user_nl_eam

 co2_conserv_error_tol_per_year = 5.e-7

 nhtfrq =  0, -24, -3, -3, 0 
 mfilt  = 1, 365, 120, 120, 1
 avgflag_pertape = 'A','A','I','A', 'I'
 fexcl1 = 'CFAD_SR532_CAL','ANSNOW','ANRAIN','AQSNOW','AQRAIN','SNOWQM'
 fincl1 = 'RHREFHT','DF_O3','AQSO4_O3','AQSO4_H2O2','TREFHTMN:M','TREFHTMX:X','FLUT','PRECT','PRECC','U200','U850','TMQ','OMEGA500','IEFLX' 
 fincl2 = 'U200','U850','V200','V850','Z500','UBOT','VBOT','OMEGA500','TREFHT','TS','TMQ','TREFHTMN:M','TREFHTMX:X','QREFHT','RHREFHT','PS','PSL','PRECT','PRECC','PRECSC','PRECSL','SNOWHLND','SNOWHICE','FLUT'
 fincl3 = 'PSL','T200','T500','U850','V850','UBOT','VBOT','TREFHT','TMQ' 
 fincl4 = 'FLNT','FSNT','U200','U850','OMEGA500','PRECT','PRECC','FSDS','FSNS','FLDS','FLNS','SHFLX','LHFLX','QFLX','TS','TBOT','QBOT','TREFHT','QREFHT','PBLH','TUQ','TVQ','TUH','TVH','DTENDTQ','DTENDTH','FSNTC','FLNTC','FSNSC','FLNSC','CLDTOT','TGCLDLWP','TGCLDIWP'
 fincl5 = 'TMCO2_LND','TMCO2_OCN','TMCO2_FFF','TMCO2'

 co2_flag = .true.
 clubb_tk1 = 268.15D0
 gw_convect_hcf = 10.0
 se_fv_phys_remap_alg = 1

 ieflx_opt = 2
 co2_readFlux_fuel = .true.
 co2flux_fuel_file = '/lcrc/group/e3sm/public_html/inputdata/atm/cam/ggas/ne30pg2_eam_CO2-em-anthro_input4MIPs_emissions_CMIP_CEDS-2017-05-18_gr_175001-201412_c20201111.nc'
 co2_readFlux_ocn = .true.
 co2flux_ocn_file = '/lcrc/group/e3sm/public_html/inputdata/atm/cam/ggas/ne30pg2_CSEM_historical_ocean_flux_1849-2014_c20240225.nc'

 co2_readFlux_aircraft = .True.
 aircraft_specifier = 'ac_CO2         -> filelist_FUELBURN_hist_ne30pg2.txt' !include aircraft emission file name ne30pg2_eam_CO2-em-AIR-anthro_input4MIPs_emissions_CMIP_CEDS-2017-08-30_gr_175001-201412_c20201111.nc
 aircraft_datapath  =  '/lcrc/group/e3sm/public_html/inputdata/atm/cam/ggas'
 aircraft_type = 'SERIAL'

EOF

cat << EOF >> user_nl_elm
  check_finidat_fsurdat_consistency = .false.
  check_finidat_year_consistency = .false.
  do_budgets = .true.
  
  create_crop_landunit = .true.
  do_transient_crops = .true. 
  do_transient_pfts = .true.

  check_dynpft_consistency = .false.

  paramfile = '/lcrc/group/e3sm/public_html/inputdata/lnd/clm2/paramdata/clm_params_c211124.nc'
  
  
  finidat = '${RUN_REFDIR}/${RUN_REFCASE}.elm.r.${RUN_REFDATE}-00000.nc'
  
  hist_nhtfrq = 0,-24,0,0                                                                      
  hist_mfilt = 1,365,1,1
  hist_dov2xy = .true.,.true.,.false.,.false.
  hist_fincl1 = 'TOTPRODC','LEAFC_STORAGE','LEAFC_XFER','FROOTC_STORAGE','FROOTC_XFER','LIVESTEMC_STORAGE','LIVESTEMC_XFER',
               'DEADSTEMC_STORAGE','DEADSTEMC_XFER','LIVECROOTC_STORAGE','LIVECROOTC_XFER','DEADCROOTC_STORAGE','DEADCROOTC_XFER',
               'GRESP_STORAGE','GRESP_XFER','TOTPRODN','DWT_PROD100C_GAIN','DWT_PROD10C_GAIN','COL_FIRE_CLOSS','COL_FIRE_NLOSS','DWT_CLOSS',
               'DWT_NLOSS','PROD100C','PROD10C','PRODUCT_CLOSS','PROD1N','PROD10N','PROD100N','PRODUCT_NLOSS','PROD1N_LOSS','PROD10N_LOSS',
               'PROD100N_LOSS','COL_FIRE_NLOSS','NET_NMIN','LEAFN_TO_LITTER','FROOTN_TO_LITTER','M_NPOOL_TO_LITTER','M_RETRANSN_TO_LITTER',
               'M_LEAFN_TO_LITTER','M_LEAFN_STORAGE_TO_LITTER','M_LEAFN_XFER_TO_LITTER','M_FROOTN_TO_LITTER','M_FROOTN_STORAGE_TO_LITTER',
               'M_FROOTN_XFER_TO_LITTER','M_LIVESTEMN_TO_LITTER','M_LIVESTEMN_STORAGE_TO_LITTER','M_LIVESTEMN_XFER_TO_LITTER','M_DEADSTEMN_TO_LITTER',
               'M_DEADSTEMN_STORAGE_TO_LITTER', 'M_DEADSTEMN_XFER_TO_LITTER','M_LIVECROOTN_TO_LITTER','M_LIVECROOTN_STORAGE_TO_LITTER',
               'M_LIVECROOTN_XFER_TO_LITTER','M_DEADCROOTN_TO_LITTER','M_DEADCROOTN_STORAGE_TO_LITTER','M_DEADCROOTN_XFER_TO_LITTER',
               'M_DEADSTEMN_TO_LITTER_FIRE','M_DEADCROOTN_TO_LITTER_FIRE','LEAFN_STORAGE','LEAFN_XFER','LIVESTEMN_STORAGE','LIVESTEMN_XFER',
               'DEADSTEMN_STORAGE','DEADSTEMN_XFER','LIVECROOTN_STORAGE','LIVECROOTN_XFER','DEADCROOTN_STORAGE','DEADCROOTN_XFER','FROOTN_STORAGE',
               'FROOTN_XFER','LEAFC_XFER_TO_LEAFC','CPOOL_TO_LEAFC','LIVESTEMC_XFER_TO_LIVESTEMC','CPOOL_TO_LIVESTEMC','DEADSTEMC_XFER_TO_DEADSTEMC',
               'CPOOL_TO_DEADSTEMC','CPOOL_TO_LIVECROOTC','CPOOL_TO_DEADCROOTC','LIVECROOTC_XFER_TO_LIVECROOTC','DEADCROOTC_XFER_TO_DEADCROOTC',
               'CPOOL_TO_FROOTC','FROOTC_XFER_TO_FROOTC','FROOT_MR','LIVESTEM_MR','LIVECROOT_MR','CPOOL_LEAF_GR','CPOOL_LEAF_STORAGE_GR',
               'TRANSFER_LEAF_GR','LITFIRE','SOMFIRE','VEGFIRE','FROOTC_TO_LITTER','M_LEAFC_TO_LITTER','M_LEAFC_STORAGE_TO_LITTER',
               'M_LEAFC_XFER_TO_LITTER','M_FROOTC_TO_LITTER','M_FROOTC_STORAGE_TO_LITTER','M_FROOTC_XFER_TO_LITTER','M_LIVESTEMC_TO_LITTER',
               'M_LIVESTEMC_STORAGE_TO_LITTER','M_LIVESTEMC_XFER_TO_LITTER','M_DEADSTEMC_TO_LITTER','M_DEADSTEMC_STORAGE_TO_LITTER',
               'M_DEADSTEMC_XFER_TO_LITTER','M_LIVECROOTC_TO_LITTER','M_LIVECROOTC_STORAGE_TO_LITTER','M_LIVECROOTC_XFER_TO_LITTER',
               'M_DEADCROOTC_TO_LITTER','M_DEADCROOTC_STORAGE_TO_LITTER','M_DEADCROOTC_XFER_TO_LITTER','M_LEAFC_TO_LITTER_FIRE',
               'M_LEAFC_STORAGE_TO_LITTER_FIRE','M_LEAFC_XFER_TO_LITTER_FIRE','M_FROOTC_TO_LITTER_FIRE','M_FROOTC_STORAGE_TO_LITTER_FIRE',
               'M_FROOTC_XFER_TO_LITTER_FIRE','M_LIVESTEMC_TO_LITTER_FIRE','M_LIVESTEMC_STORAGE_TO_LITTER_FIRE','M_LIVESTEMC_XFER_TO_LITTER_FIRE',
               'M_DEADSTEMC_TO_LITTER_FIRE','M_DEADSTEMC_STORAGE_TO_LITTER_FIRE','M_DEADSTEMC_XFER_TO_LITTER_FIRE','M_LIVECROOTC_STORAGE_TO_LITTER_FIRE',
               'M_DEADCROOTC_STORAGE_TO_LITTER_FIRE','M_GRESP_STORAGE_TO_LITTER_FIRE','M_GRESP_XFER_TO_LITTER_FIRE','M_CPOOL_TO_LITTER_FIRE',
               'M_LIVEROOTC_TO_LITTER_FIRE','M_LIVEROOTC_TO_LITTER_FIRE','M_LIVEROOTC_XFER_TO_LITTER_FIRE','M_DEADROOTC_TO_LITTER_FIRE',
               'M_DEADROOTC_XFER_TO_LITTER_FIRE','GAP_NLOSS_LITTER','FIRE_NLOSS_LITTER','HRV_NLOSS_LITTER','SEN_NLOSS_LITTER','GAP_PLOSS_LITTER',
               'FIRE_PLOSS_LITTER','HRV_PLOSS_LITTER','SEN_PLOSS_LITTER','FSRND','FSRNI','FSRVD','FSRVI',
               'CPOOL_FROOT_GR','CPOOL_FROOT_STORAGE_GR','TRANSFER_FROOT_GR','CPOOL_LIVESTEM_GR','CPOOL_LIVESTEM_STORAGE_GR','TRANSFER_LIVESTEM_GR',
               'CPOOL_DEADSTEM_GR','CPOOL_DEADSTEM_STORAGE_GR','TRANSFER_DEADSTEM_GR','CPOOL_LIVECROOT_GR','CPOOL_LIVECROOT_STORAGE_GR','TRANSFER_LIVECROOT_GR',
               'CPOOL_DEADCROOT_GR','CPOOL_DEADCROOT_STORAGE_GR','TRANSFER_DEADCROOT_GR','M_GRESP_STORAGE_TO_LITTER','M_GRESP_XFER_TO_LITTER','M_CPOOL_TO_FIRE',
               'NPOOL','NPOOL_TO_LEAFN','NPOOL_TO_FROOTN','NPOOL_TO_LIVESTEMN','NPOOL_TO_DEADSTEMN','NPOOL_TO_LIVECROOTN','NPOOL_TO_DEADCROOTN',
               'LEAFN_XFER_TO_LEAFN','FROOTN_XFER_TO_FROOTN','LIVESTEMN_XFER_TO_LIVESTEMN','DEADSTEMN_XFER_TO_DEADSTEMN','LIVECROOTN_XFER_TO_LIVECROOTN',
               'DEADCROOTN_XFER_TO_DEADCROOTN','TOTPRODP','LEAFP_STORAGE','LEAFP_XFER','FROOTP_STORAGE','FROOTP_XFER','LIVESTEMP_STORAGE','LIVESTEMP_XFER',
               'DEADSTEMP_STORAGE','DEADSTEMP_XFER','LIVECROOTP_STORAGE','LIVECROOTP_XFER','DEADCROOTP_STORAGE','DEADCROOTP_XFER','PPOOL','PPOOL_TO_LEAFP',
               'PPOOL_TO_FROOTP','PPOOL_TO_LIVESTEMP','PPOOL_TO_DEADSTEMP','PPOOL_TO_LIVECROOTP','PPOOL_TO_DEADCROOTP','LEAFP_XFER_TO_LEAFP',
               'FROOTP_XFER_TO_FROOTP','LIVESTEMP_XFER_TO_LIVESTEMP','DEADSTEMP_XFER_TO_DEADSTEMP','LIVECROOTP_XFER_TO_LIVECROOTP',
               'DEADCROOTP_XFER_TO_DEADCROOTP','FAREA_BURNED','NFIRE','AR','CPOOL'
  hist_fincl2 = 'QRUNOFF_R','TWS','SOILWATER_10CM','QSOIL', 'QVEGE', 'QVEGT','GPP','QRUNOFF'
  hist_fincl3 = 'GPP','NEE','NEP','NPP','TLAI','TOTVEGC','TOTVEGN','TOTVEGP','FROOTC','FROOTN','FROOTP','LIVECROOTC','LIVECROOTN','LIVECROOTP','DEADCROOTC','DEADCROOTN','DEADCROOTP','LIVESTEMC','LIVESTEMN','LIVESTEMP','DEADSTEMC','DEADSTEMN','DEADSTEMP','TOTPFTC','TOTPFTN','TOTPFTP','PFT_FIRE_CLOSS','PFT_FIRE_NLOSS','PFT_FIRE_PLOSS','AR','HR','PCT_LANDUNIT','PCT_NAT_PFT'
  hist_fincl4 = 'TOTLITC','TOTLITN','TOTLITP','CWDC','CWDN','CWDP','DWT_CLOSS','DWT_NLOSS','DWT_PLOSS','HR','TOTCOLC','TOTCOLN','TOTCOLP','TOTECOSYSC','TOTECOSYSN','TOTECOSYSP','TOTSOMC','TOTSOMN','TOTSOMP'
EOF

cat << EOF >> user_nl_mosart
 rtmhist_fincl2 = 'RIVER_DISCHARGE_OVER_LAND_LIQ'
 rtmhist_mfilt = 1,365
 rtmhist_ndens = 2
 rtmhist_nhtfrq = 0,-24
EOF

cat << EOF >> user_nl_docn
 taxmode = "extend"
EOF

cat <<EOF >> user_nl_cpl
  histaux_a2x3hr  = .true. 
EOF

}

patch_mpas_streams() {

echo

}

######################################################
### Most users won't need to change anything below ###
######################################################

#-----------------------------------------------------
fetch_code() {

    if [ "${do_fetch_code,,}" != "true" ]; then
        echo $'\n----- Skipping fetch_code -----\n'
        return
    fi

    echo $'\n----- Starting fetch_code -----\n'
    local path=${CODE_ROOT}
    local repo=e3sm

    echo "Cloning $repo repository branch $BRANCH under $path"
    if [ -d "${path}" ]; then
        echo "ERROR: Directory already exists. Not overwriting"
        exit 20
    fi
    mkdir -p ${path}
    pushd ${path}

    # This will put repository, with all code
    git clone git@github.com:E3SM-Project/${repo}.git .
    
    # Setup git hooks
    rm -rf .git/hooks
    git clone git@github.com:E3SM-Project/E3SM-Hooks.git .git/hooks
    git config commit.template .git/hooks/commit.template

    # Check out desired branch
    git checkout ${BRANCH}

    # Custom addition
    if [ "${CHERRY}" != "" ]; then
        echo ----- WARNING: adding git cherry-pick -----
        for commit in "${CHERRY[@]}"
        do
            echo ${commit}
            git cherry-pick ${commit}
        done
        echo -------------------------------------------
    fi

    # Bring in all submodule components
    git submodule update --init --recursive

    popd
}

#-----------------------------------------------------
create_newcase() {

    if [ "${do_create_newcase,,}" != "true" ]; then
        echo $'\n----- Skipping create_newcase -----\n'
        return
    fi

    echo $'\n----- Starting create_newcase -----\n'

    ${CODE_ROOT}/cime/scripts/create_newcase \
        --case ${CASE_NAME} \
        --case-group ${CASE_GROUP} \
        --output-root ${CASE_ROOT} \
        --script-root ${CASE_SCRIPTS_DIR} \
        --handle-preexisting-dirs u \
        --compset ${COMPSET} \
        --res ${RESOLUTION} \
        --machine ${MACHINE} \
        --project ${PROJECT} \
        --walltime ${WALLTIME} \
	--queue ${IFDEBUG} \
        --pecount ${PELAYOUT}

    if [ $? != 0 ]; then
      echo $'\nNote: if create_newcase failed because sub-directory already exists:'
      echo $'  * delete old case_script sub-directory'
      echo $'  * or set do_newcase=false\n'
      exit 35
    fi

}

modify_pe_layout() {

    if [ "${do_modify_pe_layout,,}" != "true" ]; then
        echo $'\n----- Skipping changing PE-layout -----\n'
        return
    fi

    pushd ${CASE_SCRIPTS_DIR}

    ./xmlchange MAX_MPITASKS_PER_NODE=64
    ./xmlchange MAX_TASKS_PER_NODE=64

    ./xmlchange NTASKS_WAV=1
    ./xmlchange NTASKS_GLC=1

    ./xmlchange NTHRDS_ATM=1
    ./xmlchange NTHRDS_CPL=1
    ./xmlchange NTHRDS_OCN=1
    ./xmlchange NTHRDS_WAV=1
    ./xmlchange NTHRDS_GLC=1
    ./xmlchange NTHRDS_ICE=1
    ./xmlchange NTHRDS_ROF=1
    ./xmlchange NTHRDS_LND=1

    ./xmlchange ROOTPE_ATM=0
    ./xmlchange ROOTPE_CPL=0
    ./xmlchange ROOTPE_OCN=0
    ./xmlchange ROOTPE_WAV=0
    ./xmlchange ROOTPE_GLC=0
    ./xmlchange ROOTPE_ICE=0
    ./xmlchange ROOTPE_ROF=0
    ./xmlchange ROOTPE_LND=0

    if [[ ${PELAYOUT} == "M" ]]; then
        echo $'\n----- changing PE layout to M -----\n'
        ./xmlchange NTASKS_ATM=1350
        ./xmlchange NTASKS_CPL=1408
        ./xmlchange NTASKS_OCN=1408
        ./xmlchange NTASKS_ICE=1408
        ./xmlchange NTASKS_ROF=1408
        ./xmlchange NTASKS_LND=1408
    elif [[ ${PELAYOUT} == "S" ]]; then
        echo $'\n----- changing PE layout to S -----\n'
        ./xmlchange NTASKS_ATM=1080
        ./xmlchange NTASKS_CPL=1280
        ./xmlchange NTASKS_OCN=1280
        ./xmlchange NTASKS_ICE=1280
        ./xmlchange NTASKS_ROF=1280
        ./xmlchange NTASKS_LND=1280
    elif [[ ${PELAYOUT} == "L" ]]; then
        echo $'\n----- changing PE layout to L -----\n'
        ./xmlchange NTASKS_ATM=2700
        ./xmlchange NTASKS_CPL=2752
        ./xmlchange NTASKS_OCN=2752
        ./xmlchange NTASKS_ICE=2752
        ./xmlchange NTASKS_ROF=2752
        ./xmlchange NTASKS_LND=2752
    elif [[ ${PELAYOUT} == "XL" ]]; then
        echo $'\n----- changing PE layout to XL -----\n'
        ./xmlchange NTASKS_ATM=5400
        ./xmlchange NTASKS_CPL=5440
        ./xmlchange NTASKS_OCN=5440
        ./xmlchange NTASKS_ICE=5440
        ./xmlchange NTASKS_ROF=5440
        ./xmlchange NTASKS_LND=5440
    else
        echo 'ERROR: $PELAYOUT = '${PELAYOUT}' but no layout exists for this setting.'
        exit 297
    fi

    popd
}

#-----------------------------------------------------
case_setup() {

    if [ "${do_case_setup,,}" != "true" ]; then
        echo $'\n----- Skipping case_setup -----\n'
        return
    fi

    echo $'\n----- Starting case_setup -----\n'
    pushd ${CASE_SCRIPTS_DIR}

    # Setup some CIME directories
    ./xmlchange EXEROOT=${CASE_BUILD_DIR}
    ./xmlchange RUNDIR=${CASE_RUN_DIR}

    # Short term archiving
    ./xmlchange DOUT_S=${DO_SHORT_TERM_ARCHIVING^^}
    ./xmlchange DOUT_S_ROOT=${CASE_ARCHIVE_DIR}
    
    # using custom layout for cori-kn
    ./xmlchange --file env_mach_pes.xml --id MAX_TASKS_PER_NODE --val 64
    ./xmlchange --file env_mach_pes.xml --id MAX_MPITASKS_PER_NODE --val 64
    declare -a comps=("ATM" "CPL" "LND" "ICE" "OCN" "GLC" "ROF" "WAV" "ESP" )
    for thiscomp in "${comps[@]}"; do
      ./xmlchange --file env_mach_pes.xml --id NTHRDS_$thiscomp --val 1
    done

    # Build with COSP, except for a data atmosphere (datm)
    if [ `./xmlquery --value COMP_ATM` == "datm"  ]; then 
      echo $'\nThe specified configuration uses a data atmosphere, so cannot activate COSP simulator\n'
    else
      echo $'\nConfiguring E3SM to use the COSP simulator\n'
      ./xmlchange --id CAM_CONFIG_OPTS --append --val='-cosp'
    fi

    # Turn on co2-cycle for temeporay solution. - sf 1/14/2022
    #./xmlchange --append CAM_CONFIG_OPTS='-co2_cycle'
    
    # Extracts input_data_dir in case it is needed for user edits to the namelist later
    local input_data_dir=`./xmlquery DIN_LOC_ROOT --value`

    # Custom user_nl
    user_nl

    # Finally, run CIME case.setup
    ./case.setup --reset

    popd
}

#-----------------------------------------------------
case_build() {

    pushd ${CASE_SCRIPTS_DIR}

    # do_case_build = false
    if [ "${do_case_build,,}" != "true" ]; then

        echo $'\n----- case_build -----\n'

        if [ "${OLD_EXECUTABLE}" == "" ]; then
            # Ues previously built executable, make sure it exists
            if [ -x ${CASE_BUILD_DIR}/e3sm.exe ]; then
                echo 'Skipping build because $do_case_build = '${do_case_build}
            else
                echo 'ERROR: $do_case_build = '${do_case_build}' but no executable exists for this case.'
                exit 297
            fi
        else
            # If absolute pathname exists and is executable, reuse pre-exiting executable
            if [ -x ${OLD_EXECUTABLE} ]; then
                echo 'Using $OLD_EXECUTABLE = '${OLD_EXECUTABLE}
                cp -fp ${OLD_EXECUTABLE} ${CASE_BUILD_DIR}/
            else
                echo 'ERROR: $OLD_EXECUTABLE = '$OLD_EXECUTABLE' does not exist or is not an executable file.'
                exit 297
            fi
        fi
        echo 'WARNING: Setting BUILD_COMPLETE = TRUE.  This is a little risky, but trusting the user.'
        ./xmlchange BUILD_COMPLETE=TRUE

    # do_case_build = true
    else

        echo $'\n----- Starting case_build -----\n'

        # Turn on debug compilation option if requested
        if [ "${DEBUG_COMPILE^^}" == "TRUE" ]; then
            ./xmlchange DEBUG=${DEBUG_COMPILE^^}
        fi

        # Run CIME case.build
        ./case.build

        # Some user_nl settings won't be updated to *_in files under the run directory
        # Call preview_namelists to make sure *_in and user_nl files are consistent.
        ./preview_namelists

    fi

    popd
}

#-----------------------------------------------------
runtime_options() {
    
    source /lcrc/soft/climate/e3sm-unified/load_latest_e3sm_unified_chrysalis.sh

    echo $'\n----- Starting runtime_options -----\n'
    pushd ${CASE_SCRIPTS_DIR}

    # Set simulation start date
    ./xmlchange RUN_STARTDATE=${START_DATE}

    # Segment length
    ./xmlchange STOP_OPTION=${STOP_OPTION,,},STOP_N=${STOP_N}

    # Restart frequency
    ./xmlchange REST_OPTION=${REST_OPTION,,},REST_N=${REST_N}

    # Coupler history
    ./xmlchange HIST_OPTION=${HIST_OPTION,,},HIST_N=${HIST_N}

    # Coupler budgets (always on)
    ./xmlchange BUDGETS=TRUE

    # Set resubmissions
    if (( RESUBMIT > 0 )); then
        ./xmlchange RESUBMIT=${RESUBMIT}
    fi

    # Run type
    # Start from default of user-specified initial conditions
    if [ "${MODEL_START_TYPE,,}" == "initial" ]; then
        ./xmlchange RUN_TYPE="startup"
        ./xmlchange CONTINUE_RUN="FALSE"

    # Continue existing run
    elif [ "${MODEL_START_TYPE,,}" == "continue" ]; then
        ./xmlchange CONTINUE_RUN="TRUE"

    elif [ "${MODEL_START_TYPE,,}" == "branch" ] || [ "${MODEL_START_TYPE,,}" == "hybrid" ]; then
        ./xmlchange RUN_TYPE=${MODEL_START_TYPE}
        ./xmlchange GET_REFCASE=${GET_REFCASE}
	./xmlchange RUN_REFDIR=${RUN_REFDIR}
        ./xmlchange RUN_REFCASE=${RUN_REFCASE}
        ./xmlchange RUN_REFDATE=${RUN_REFDATE}
        echo 'Warning: $MODEL_START_TYPE = '${MODEL_START_TYPE} 
	echo '$RUN_REFDIR = '${RUN_REFDIR}
	echo '$RUN_REFCASE = '${RUN_REFCASE}
	echo '$RUN_REFDATE = '${START_DATE}
        
	ln -sf  ${RUN_REFDIR}/${RUN_REFCASE}.eam.i.${RUN_REFDATE}-00000.nc ${CASE_RUN_DIR}/.
	ln -sf  ${RUN_REFDIR}/${RUN_REFCASE}.eam.r.${RUN_REFDATE}-00000.nc ${CASE_RUN_DIR}/.
	ln -sf  ${RUN_REFDIR}/${RUN_REFCASE}.eam.rs.${RUN_REFDATE}-00000.nc ${CASE_RUN_DIR}/.
	ln -sf  ${RUN_REFDIR}/${RUN_REFCASE}.elm.r.${RUN_REFDATE}-00000.nc ${CASE_RUN_DIR}/.
	ln -sf  ${RUN_REFDIR}/${RUN_REFCASE}.elm.rh0.${RUN_REFDATE}-00000.nc ${CASE_RUN_DIR}/.
	ln -sf  ${RUN_REFDIR}/${RUN_REFCASE}.cpl.r.${RUN_REFDATE}-00000.nc ${CASE_RUN_DIR}/.
	ln -sf  ${RUN_REFDIR}/${RUN_REFCASE}.docn.rs1.${RUN_REFDATE}-00000.bin ${CASE_RUN_DIR}/.
	ln -sf  ${RUN_REFDIR}/${RUN_REFCASE}.mosart.r.${RUN_REFDATE}-00000.nc ${CASE_RUN_DIR}/.
	ln -sf  ${RUN_REFDIR}/${RUN_REFCASE}.mosart.rh0.${RUN_REFDATE}-00000.nc ${CASE_RUN_DIR}/.
	ln -sf  ${RUN_REFDIR}/${RUN_REFCASE}.mosart.rh1.${RUN_REFDATE}-00000.nc ${CASE_RUN_DIR}/.
	cp  ${RUN_REFDIR}/${RUN_REFCASE}.mpassi.rst.${RUN_REFDATE}_00000.nc ${CASE_RUN_DIR}/.
	ncrename -v xtime,xtime.orig ${CASE_RUN_DIR}/${RUN_REFCASE}.mpassi.rst.${RUN_REFDATE}_00000.nc

	cp ${RUN_REFDIR}/rpointer.atm ${CASE_RUN_DIR}/
	cp ${RUN_REFDIR}/rpointer.lnd ${CASE_RUN_DIR}/
	cp ${RUN_REFDIR}/rpointer.ocn ${CASE_RUN_DIR}/
	cp ${RUN_REFDIR}/rpointer.ice ${CASE_RUN_DIR}/
	cp ${RUN_REFDIR}/rpointer.drv ${CASE_RUN_DIR}/
	cp ${RUN_REFDIR}/rpointer.rof ${CASE_RUN_DIR}/
    else
        echo 'ERROR: $MODEL_START_TYPE = '${MODEL_START_TYPE}' is unrecognized. Exiting.'
        exit 380
    fi

    # docn setup
    ./xmlchange --id PIO_TYPENAME  --val "pnetcdf"
    ./xmlchange --id SSTICE_DATA_FILENAME  --val "/lcrc/group/e3sm/public_html/inputdata/ocn/docn7/SSTDATA/sst_ice_CMIP6_DECK_E3SM_1x1_c20191207.nc"
    ./xmlchange --id SSTICE_YEAR_ALIGN  --val "1869"
    ./xmlchange --id SSTICE_YEAR_START  --val "1869"
    ./xmlchange --id SSTICE_YEAR_END  --val "2016"

    # Patch mpas streams files
    patch_mpas_streams

    # modify to use priority queue 

   if [ "${run}" != "production" ]; then

   ./xmlchange --file env_workflow.xml --id CHARGE_ACCOUNT --val "priority"
   ./xmlchange --file env_workflow.xml --id PROJECT --val "priority"
   ./xmlchange --file env_workflow.xml --id JOB_QUEUE --force --val "priority"
   fi
   popd
}

#-----------------------------------------------------
case_submit() {

    if [ "${do_case_submit,,}" != "true" ]; then
        echo $'\n----- Skipping case_submit -----\n'
        return
    fi

    echo $'\n----- Starting case_submit -----\n'
    pushd ${CASE_SCRIPTS_DIR}
    
    # Run CIME case.submit
    ./case.submit

    popd
}

#-----------------------------------------------------
copy_script() {

    echo $'\n----- Saving run script for provenance -----\n'

    local script_provenance_dir=${CASE_SCRIPTS_DIR}/run_script_provenance
    mkdir -p ${script_provenance_dir}
    local this_script_name=`basename $0`
    local script_provenance_name=${this_script_name}.`date +%Y%m%d-%H%M%S`
    cp -vp ${this_script_name} ${script_provenance_dir}/${script_provenance_name}

}

#-----------------------------------------------------
# Silent versions of popd and pushd
pushd() {
    command pushd "$@" > /dev/null
}
popd() {
    command popd "$@" > /dev/null
}

# Now, actually run the script
#-----------------------------------------------------
main
