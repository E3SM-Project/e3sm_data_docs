Generating tables
=================

Relevant `utils` files: `generate_tables.py`, `generate_html.bash`

```
$ cd utils
$ ./generate_html.bash
```

Creating reproduction scripts
=============================

Relevant `utils` files: `diff_patch`, `generate_reproduction_script.bash`, `patch_helper.py`, `update_reproduction_scripts.bash`

```
$ resolution=<resolution>
$ case_name=<case_name>
$ cd ~/e3sm_data_docs/utils
$ ./generate_reproduction_script.bash ${resolution} ${case_name}
# If you are replacing an existing script, run the following to compare results:
$ diff ../run_scripts/v2/reproduce/run.v2.${resolution}.${case_name}.sh run.v2.${resolution}.${case_name}.sh
# In any case, you should review the generated script. If it looks good, then run:
$ mv run.v2.${resolution}.${case_name}.sh ../run_scripts/v2/reproduce/run.v2.${resolution}.${case_name}.sh
```

To modify all the reproduction scripts run `./update_reproduction_scripts.bash`.

Testing reproduction scripts
============================

Relevant `utils` files: `check_results.bash`, `test_reproduction_scripts.bash`

```
# IMPORTANT: Make sure the `lcrc#dtn_bebop` and `NERSC HPSS` Globus endpoints are activated
# and will stay activated for the duration of this run (24 hours)
# If this is not the case, the tests will not be able to load initial conditions (via `zstash`).
$ sbatch test_reproduction_scripts.bash

# Run the following to check if the jobs are still running:
$ squeue -o "%8u %.7a %.4D %.9P %7i %.2t %.10r %.10M %.10l %j" --sort=P,-t,-p -u ${USER}

# Once all jobs finish, run:
$ ./check_results.bash
```
