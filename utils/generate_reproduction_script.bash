# Script to generate a reproduction script.
# Give the case name as the command line argument.

resolution=${1}
case_name=${2}
script_name=run.v2.${resolution}.${case_name}.sh

cp ../run_scripts/v2/original/${script_name} ${script_name}

# Apply patch
patch ${script_name} diff_patch

# Automatically apply patches that were likely rejected
# Also, remove `piControl` instances introduced by the patch
python patch_helper.py ${script_name} ${resolution} ${case_name}
# Use the script version produced by the Python helper script.
rm ${script_name}
mv ${script_name}.edited ${script_name}
echo "Check the rejects file to see if any other patches were missed:"
cat ${script_name}.rej

# Remove ancillary files
rm ${script_name}.orig ${script_name}.rej

# Change permissions
chmod 755 ${script_name}

# Move reproduction script to the correct directory
echo "Confirm the reproduction script looks good. Then move with:"
echo "mv ${script_name} ../run_scripts/v2/reproduce/${script_name}"
