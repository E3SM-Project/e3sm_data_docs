USER_ENTRY#!/bin/sh -e
#==============================================#
# Date: 2022-12-19
#
# Description:
#
# Submission script used for a 40-day ne1024pg2
# simulation with the DYAMOND1 configuration.
#
# All versions of the code used for FourSeasons
# simulations can be found at:
#
# https://github.com/AaronDonahue/scream/releases
#
# Individual Hashes for versions:
#
#   Full Runs:    78d6bb1f8086b5aa1c13efa879ac36ea8d3c23f5
#   SHOC Tuning:  793dde7b0f45a772a641993fb4ce32a1578a214a
#   TMS:          a718a526952797af3adf08304f7d0561bc87acc7
#   Cloud Tuning: 7ab7ecaaa8d36bc908a79aa9d5d9cdd976fc1e1f
#==============================================#

## Location of eamxx codebase
# NOTE TO USER: See above notes about which version of the code to use.
eamxx_src=~/Code/scream
## Location of eamxx output control files
eamxx_out_files_root=~/Code/scream-docs
## Location of elm namelist file to use
elm_nl_file=$eamxx_out_files_root/v1_output/user_nl_elm_20221031_DYAMOND1

## Some provenance information
githash_eamxx=`git --git-dir $eamxx_src/.git rev-parse HEAD`
masterhash_eamxx=`git --git-dir $eamxx_src/.git log -n 1 --pretty=format:"%H" origin/master`
githash_screamdocs=`git --git-dir $eamxx_out_files_root/.git rev-parse HEAD`
masterhash_screamdocs=`git --git-dir $eamxx_out_files_root/.git log -n 1 --pretty=format:"%H" origin/master`

## Job size information
nnode=1024
pernode=6
ntask=$(($pernode * $nnode))

## Compset and jobname information
name=4Seasons_DYAMOND1
compset=F2010-SCREAMv1-DYAMOND1
res=ne1024pg2_ne1024pg2
cname=$name.$res.$compset.$githash_eamxx

## Job submission and compiler information
queue=batch
compiler=gnugpu
machine=summit

## Create new-case
rm -rf $cname
$eamxx_src/cime/scripts/create_newcase --case ${cname} --compset ${compset} --res ${res} \
  -mach ${machine} --compiler ${compiler} --handle-preexisting-dirs u

## Run settings
cd $cname
echo "master hash for EAMxx: $masterhash_eamxx" > GIT_INFO.txt
echo "master hash for output files: $masterhash_screamdocs" >> GIT_INFO.txt
./xmlchange JOB_QUEUE=$queue
./xmlchange JOB_WALLCLOCK_TIME=2:00:00
./xmlchange STOP_OPTION=nhours
./xmlchange STOP_N=48
./xmlchange HIST_N=99999; ./xmlchange HIST_OPTION=nyears ;
./xmlchange REST_N=48; ./xmlchange REST_OPTION=nhours ;
./xmlchange AVGHIST_OPTION=nyears
./xmlchange AVGHIST_N=1
# Using threads for LAND
./xmlchange NTASKS=$ntask
./xmlchange MAX_TASKS_PER_NODE=84    
./xmlchange MAX_MPITASKS_PER_NODE=6
./xmlchange LND_NTHRDS=14
# Note, MPI on host
./xmlchange SCREAM_CMAKE_OPTIONS="SCREAM_NUM_VERTICAL_LEV 128 SCREAM_NUM_TRACERS 10 HOMMEXX_MPI_ON_DEVICE Off"
./xmlchange PIO_NETCDF_FORMAT="64bit_data"
./xmlchange RESUBMIT=2

## Setup case
./case.setup

## EAMxx settings
./atmchange Scorpio::output_yaml_files=\
${eamxx_out_files_root}/v1_output/scream_output.Cldfrac.yaml,\
${eamxx_out_files_root}/v1_output/scream_output.QcQi.yaml,\
${eamxx_out_files_root}/v1_output/scream_output.QvT.yaml,\
${eamxx_out_files_root}/v1_output/scream_output.TOMVars.yaml,\
${eamxx_out_files_root}/v1_output/scream_output.VertIntegrals.yaml,\
${eamxx_out_files_root}/v1_output/scream_output.HorizWinds.yaml,\
${eamxx_out_files_root}/v1_output/scream_output.QrPsPsl.yaml,\
${eamxx_out_files_root}/v1_output/scream_output.SurfVars_128lev.yaml,\
${eamxx_out_files_root}/v1_output/scream_output.TkeOmega.yaml,\
${eamxx_out_files_root}/v1_output/scream_output.Temp_2m_min.yaml,\
${eamxx_out_files_root}/v1_output/scream_output.Temp_2m_max.yaml,\
${eamxx_out_files_root}/v1_output/scream_output.Qv_2m.yaml,\
${eamxx_out_files_root}/v1_output/scream_output.PresLevs.yaml

./atmchange statefreq=5184 # 2/day
./atmchange orbital_year=-9999

## ELM settings
cp ${elm_nl_file} user_nl_elm

## Build and submit
./case.build
./case.submit
