import re
import sys

def help_patch(script_name, resolution, case_name):
    pelayout_count = 0
    walltime_count = 0
    add_fsurdat = False
    with open(script_name, "r") as f_in:
        with open(f"{script_name}.edited", "w") as f_out:
            for line in f_in:
                # Exact matches
                if line == 'readonly CASE_GROUP="v2.LR"\n':
                    f_out.write('\n')
                elif line == '# Configured to reproduce v2.LR.piControl on chrysalis.\n':
                    f_out.write(f'# Configured to reproduce v2.{resolution}.{case_name} on chrysalis.\n')
                elif line == '#readonly CASE_NAME=${CHECKOUT}.piControl.${RESOLUTION}.${MACHINE}\n':
                    f_out.write(f'#readonly CASE_NAME=${{CHECKOUT}}.{case_name}.${{RESOLUTION}}.${{MACHINE}}\n')
                elif line == 'readonly CASE_NAME="v2.LR.piControl"\n':
                    f_out.write(f'readonly CASE_NAME="v2.{resolution}.{case_name}"\n')
                # General matches 
                elif line.startswith('readonly CASE_NAME='):
                    # Deletes extra occurrence of CASE_NAME
                    # Since this elif occurs after the other CASE_NAME block,
                    # that occurrence should remain.
                    f_out.write('\n')
                elif line.startswith('readonly CHECKOUT='):
                    f_out.write('readonly CHECKOUT="20221102-maint-20"\n')
                elif line.startswith('readonly BRANCH='):
                    f_out.write('readonly BRANCH="maint-2.0"\n')
                elif line.startswith('readonly CHERRY'):
                    f_out.write('readonly CHERRY=( )\n')
                elif line.startswith('readonly RUN_REFDIR'):
                    # ${CASE_NAME} includes `v2.LR.`
                    result = re.search("/lcrc/group/e3sm/(.*)/(.*)/(.*)/init", line)
                    if result:
                        init_case_name = result.group(3)
                        # Need to use init from a different case
                        f_out.write(f'readonly RUN_REFDIR="/lcrc/group/e3sm/${{USER}}/E3SMv2_test/{init_case_name}/init"\n')
                    else:
                        f_out.write('readonly RUN_REFDIR="/lcrc/group/e3sm/${USER}/E3SMv2_test/${CASE_NAME}/init"\n')
                elif line.startswith("readonly run="):
                    if (resolution == "NARRM") and ("amip" in case_name):
                        # Need to have `BUILD_THREADED = False` to match expected checksums
                        f_out.write("readonly run='M_2x5_ndays'\n")
                    else:
                        f_out.write("readonly run='XS_1x10_ndays'\n")
                elif line.startswith('  readonly PELAYOUT'):
                    if pelayout_count == 0:
                        f_out.write(line) # pelayout = 0 => write pelayout for the non-production block
                    else:
                        f_out.write('  readonly PELAYOUT="ML"\n') # pelayout = 1 => write pelayout for production block
                    pelayout_count += 1
                elif line.startswith('  readonly WALLTIME'):
                    if walltime_count == 0:
                        # walltime = 0 => write walltime for the non-production block
                        print(f"case_name={case_name}")
                        if (resolution == "NARRM") and ("amip" in case_name):
                            f_out.write('  readonly WALLTIME="4:00:00"\n')
                        else:
                            f_out.write(line)
                    else:
                        f_out.write('  readonly WALLTIME="48:00:00"\n') # walltime = 1 => write walltime for production block
                    walltime_count += 1
                elif line.startswith('  readonly REST_N'):
                    f_out.write('  readonly REST_N="1"\n')
                elif line.startswith('cat << EOF >> user_nl_elm'):
                    f_out.write(line)
                    add_fsurdat = True                    
                elif line.startswith('check_finidat_fsurdat_consistency = .false.'):
                    f_out.write(line)
                    # We already have the fsurdat line.
                    add_fsurdat = False
                elif add_fsurdat and line.startswith('EOF'):
                    f_out.write('\n')
                    f_out.write('! Override\n')
                    f_out.write('check_finidat_fsurdat_consistency = .false.\n')
                    f_out.write('\n')
                    f_out.write(line)
                    add_fsurdat = False
                elif line.startswith('        --pecount ${layout}'):
                    f_out.write('        --pecount ${layout}"\n')
                    f_out.write('\n')
                    f_out.write('    # Optional arguments\n')
                    f_out.write('    if [ ! -z "${PROJECT}" ]; then\n')
                    f_out.write('      args="${args} --project ${PROJECT}"\n')
                    f_out.write('    fi\n')
                    f_out.write('    if [ ! -z "${CASE_GROUP}" ]; then\n')
                    f_out.write('      args="${args} --case-group ${CASE_GROUP}"\n')
                    f_out.write('    fi\n')
                    f_out.write('    if [ ! -z "${QUEUE}" ]; then\n')
                    f_out.write('      args="${args} --queue ${QUEUE}"\n')
                    f_out.write('    fi\n')
                    f_out.write('\n')
                    f_out.write('    ${CODE_ROOT}/cime/scripts/create_newcase ${args}\n')
                # Keep line as is
                else:
                    f_out.write(line)
                    if "piControl" in line:
                        if not line.startswith('readonly RUN_REFCASE=') and not line.startswith('readonly OLD_EXECUTABLE='):
                            print(f"remaining piControl instance: {line}")

if __name__ == "__main__":
    script_name = sys.argv[1]
    resolution = sys.argv[2]
    case_name = sys.argv[3]
    help_patch(script_name, resolution, case_name)
