python generate_tables.py
cd ../docs/ && make html
rm -rf /global/cfs/cdirs/e3sm/www/$USER/data_docs
mv _build /global/cfs/cdirs/e3sm/www/$USER/data_docs
chmod -R o+rx /global/cfs/cdirs/e3sm/www/$USER/data_docs
