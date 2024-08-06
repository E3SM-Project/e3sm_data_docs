#python generate_tables.py
cd ../docs/ && make html
rm -rf /global/cfs/cdirs/e3sm/www/$USER/data_docs
mv _build /global/cfs/cdirs/e3sm/www/$USER/data_docs
chmod -R o+rx /global/cfs/cdirs/e3sm/www/$USER/data_docs

echo "https://portal.nersc.gov/project/e3sm/$USER/data_docs/html/v2/WaterCycle/simulation_data/simulation_table.html"
echo "https://portal.nersc.gov/project/e3sm/$USER/data_docs/html/v2/WaterCycle/reproducing_simulations/reproduction_table.html"
echo "https://portal.nersc.gov/project/e3sm/$USER/data_docs/html/v1/WaterCycle/simulation_data/simulation_table.html"
echo "https://portal.nersc.gov/project/e3sm/$USER/data_docs/html/v1/WaterCycle/reproducing_simulations/reproduction_table.html"