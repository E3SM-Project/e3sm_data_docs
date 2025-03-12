#!/bin/bash -fe

# E3SM CBGC v2 run_e3sm script template for offline land.
#
# Inspired by v1 run_e3sm script as well as SCREAM group simplified run script.
#
# Bash coding style inspired by:
# http://kfirlavi.herokuapp.com/blog/2012/11/14/defensive-bash-programming

# TO DO:
# - custom pelayout

main() {

# For debugging, uncomment line below
#set -x

# --- Configuration flags ----

# Machine and project
readonly MACHINE=chrysalis
readonly PROJECT="e3sm"

# Simulation
readonly MYDATE=$(date '+%Y%m%d')           #Date stamp for this case - default is today, but if running final spinup should be set the same as ad spinup
readonly MYDATE_REST=20220321               #Date stamp for simulation from which the restart file was generated
readonly COMPSET="I20TRGSWCNP"              
readonly COMPSET_REST="I1850GSWCNP.fnsp"    #Compset for simulation from which the restat file was generated (add .adsp or .fnsp for spinup)
readonly RESOLUTION="ne30pg2_r05_EC30to60E2r2"
readonly CASE_NAME="${MYDATE}_CBGCv2.r05.${MACHINE}.${COMPSET}"
readonly CASE_GROUP="v2.ELMtransient"

# Code and compilation
readonly CHECKOUT="20230220" #"${MYDATE}"   #Use same code as AD spinup
readonly BRANCH="acme-y9s/BGCV2_compsets"
#readonly CHERRY=( "62749be14637e41ab4e7fb004a8e135934d02624" "38243bf9533e824008671e367c0412babccf645f" ) # PR4678,4688
#readonly CHERRY=( "6221fcc" "8d7948c" "d1c3b2a")
readonly DEBUG_COMPILE=false

# Run options
readonly MODEL_START_TYPE="hybrid"  # 'initial', 'continue', 'branch', 'hybrid'
readonly START_DATE="1850-01-01"

# Additional options for 'branch' and 'hybrid'
readonly GET_REFCASE=TRUE
readonly RUN_REFCASE="${MYDATE_REST}_CBGCv2.r05.${MACHINE}.${COMPSET_REST}"     
#readonly RUN_REFDIR="/lcrc/group/e3sm/${USER}/E3SMv2/${RUN_REFCASE}/run"
RUN_REFDIR="/lcrc/group/e3sm/data/inputdata/e3sm_init/BGCv2_land_init/${MYDATE_REST}_CBGCv2.r05.${MACHINE}.${COMPSET_REST}"
readonly RUN_REFDATE="0601-01-01"   # same as MODEL_START_DATE for 'branch', can be different for 'hybrid'

# Set paths
readonly CODE_ROOT="${HOME}/E3SMv2/code/${CHECKOUT}"
readonly CASE_ROOT="/lcrc/group/e3sm/${USER}/E3SMv2/${CASE_NAME}"

# Sub-directories
readonly CASE_BUILD_DIR=${CASE_ROOT}/build
readonly CASE_ARCHIVE_DIR=${CASE_ROOT}/archive

# Define type of run
#  short tests: 'XS_2x5_ndays', 'XS_1x10_ndays', 'S_1x10_ndays', 
#               'M_1x10_ndays', 'M2_1x10_ndays', 'M80_1x10_ndays', 'L_1x10_ndays'
#  or 'production' for full simulation
readonly run='production' # xs < 20 nodes => fits in debug queue. M80 uses 80 nodes, L uses 105.
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
  readonly WALLTIME="2:00:00"
  readonly STOP_OPTION=${units}
  readonly STOP_N=${length}
  readonly REST_OPTION=${STOP_OPTION}
  readonly REST_N=${STOP_N}
  readonly RESUBMIT=${resubmit}
  readonly DO_SHORT_TERM_ARCHIVING=false

else

  # Production simulation
  readonly CASE_SCRIPTS_DIR=${CASE_ROOT}/case_scripts
  readonly CASE_RUN_DIR=${CASE_ROOT}/run
  readonly PELAYOUT="5120"
  readonly WALLTIME="24:00:00"
  readonly STOP_OPTION="nyears"
  readonly STOP_N=70 # How often to stop the model, should be a multiple of REST_N
  readonly REST_OPTION="nyears"
  readonly REST_N="10" # How often to write a restart file
  readonly RESUBMIT="0" # Submissions after initial one
  readonly DO_SHORT_TERM_ARCHIVING=false
fi

# Coupler history 
readonly HIST_OPTION="nyears"
readonly HIST_N="20"

# Leave empty (unless you understand what it does)
readonly OLD_EXECUTABLE=""

# --- Toggle flags for what to do ----
do_fetch_code=false
do_create_newcase=true
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

}

# =======================
# Custom user_nl settings
# =======================

user_nl() {

cat << EOF >> user_nl_elm
  check_finidat_fsurdat_consistency = .false.
  check_finidat_year_consistency = .false.
  flanduse_timeseries='/lcrc/group/e3sm/ccsm-data/inputdata/lnd/clm2/surfdata_map/landuse.timeseries_0.5x0.5_HIST_simyr1850-2015_c230702_noC3grass_2cells.nc'
  do_budgets = .true.
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
    #git clone git@github.com:E3SM-Project/${repo}.git .
    git clone https://github.com/E3SM-Project/${repo}.git .

    # Setup git hooks
    rm -rf .git/hooks
    #git clone git@github.com:E3SM-Project/E3SM-Hooks.git .git/hooks
    git clone https://github.com/E3SM-Project/E3SM-Hooks.git ./git/hooks
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
        --pecount ${PELAYOUT}

    if [ $? != 0 ]; then
      echo $'\nNote: if create_newcase failed because sub-directory already exists:'
      echo $'  * delete old case_script sub-directory'
      echo $'  * or set do_newcase=false\n'
      exit 35
    fi

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

    # 80 nodes for DATM
    declare -a comps=("ATM" "CPL" "LND" "ICE" "OCN" "GLC" "ROF" "WAV" "ESP" )
    for thiscomp in "${comps[@]}"; do
      ./xmlchange -file env_mach_pes.xml -id NTASKS_$thiscomp -val 5120
      ./xmlchange -file env_mach_pes.xml -id NTHRDS_$thiscomp -val 1
    done
    ./xmlchange -file env_mach_pes.xml -id MAX_TASKS_PER_NODE -val 64
    ./xmlchange -file env_mach_pes.xml -id MAX_MPITASKS_PER_NODE -val 64

    #Align year for transient simulation
    ./xmlchange -file env_run.xml      -id DATM_CLMNCEP_YR_ALIGN -val 1841
    # Accelerated decomp spinup
    #./xmlchange -file env_run.xml -id ELM_BLDNML_OPTS --append -val "-bgc_spinup on"

    # Build with COSP, except for a data atmosphere (datm)
    if [ `./xmlquery --value COMP_ATM` == "datm"  ]; then 
      echo $'\nThe specified configuration uses a data atmosphere, so cannot activate COSP simulator\n'
    else
      echo $'\nConfiguring E3SM to use the COSP simulator\n'
      ./xmlchange --id CAM_CONFIG_OPTS --append --val='-cosp'
    fi
 
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
        ./xmlchange RUN_TYPE=${MODEL_START_TYPE,,}
        ./xmlchange GET_REFCASE=${GET_REFCASE}
	./xmlchange RUN_REFDIR=${RUN_REFDIR}
        ./xmlchange RUN_REFCASE=${RUN_REFCASE}
        ./xmlchange RUN_REFDATE=${RUN_REFDATE}
        echo 'Warning: $MODEL_START_TYPE = '${MODEL_START_TYPE} 
	echo '$RUN_REFDIR = '${RUN_REFDIR}
	echo '$RUN_REFCASE = '${RUN_REFCASE}
	echo '$RUN_REFDATE = '${START_DATE}
 
    else
        echo 'ERROR: $MODEL_START_TYPE = '${MODEL_START_TYPE}' is unrecognized. Exiting.'
        exit 380
    fi

    # Patch mpas streams files
    patch_mpas_streams

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
