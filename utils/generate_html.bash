pr_num=60
try_num=9

# Chrysalis
#destination_dir=/lcrc/group/e3sm/public_html/diagnostic_output/$USER/data_docs_${pr_num}
#web_page="https://web.lcrc.anl.gov/public/e3sm/diagnostic_output/$USER/data_docs_${pr_num}/html/"
# Perlmutter
destination_dir=/global/cfs/cdirs/e3sm/www/$USER/data_docs_${pr_num}_try${try_num}
web_page="https://portal.nersc.gov/cfs/e3sm/$USER/data_docs_${pr_num}_try${try_num}/html/"

python generate_tables.py
if [ $? != 0 ]; then
  exit 1
fi
cd ../docs/ && make html
rm -rf ls ${destination_dir}
mv _build ${destination_dir}
chmod -R o+rx ${destination_dir}
echo "Go to: ${web_page}"
