# Setup project repo and generate figures

# DS5110 Fall 2023 Project Team 8 SDG

# 2023-11-07

# Lukas Hernandez <hernandez.lu@northeastern.edu>
# Johnathan Green <green.john@northeastern.edu>
# Ryan Moore <moore.will@northeastern.edu>

tides_demo:
	python -B src/tides_demo.py

tides_visuals: clean_tides_visuals_imgs figs/avg_monthly_temps_from_2009.png

figs/avg_monthly_temps_from_2009.png: figs
	python -B src/tides_visualizations.py

download_all_noaa_tides_data: rm_clean_data raw_data data
	python -B src/download_noaa_tides_data.py all all clean

download_portland_all_noaa_tides_data: rm_portland_clean raw_data data
	python -B src/download_noaa_tides_data.py all 8418150 clean

download_eastport_all_noaa_tides_data: rm_eastport_clean raw_data data
	python -B src/download_noaa_tides_data.py all 8410140 clean

download_cutler_farris_wharf_all_noaa_tides_data: rm_cfw_clean raw_data data
	python -B src/download_noaa_tides_data.py all 8411060 clean

download_seavey_island_all_noaa_tides_data: rm_si_clean raw_data data
	python -B src/download_noaa_tides_data.py all 8419870 clean

download_bar_harbor_noaa_tides_data: rm_bh_clean raw_data data
	python -B src/download_noaa_tides_data.py all 8413320 clean

get_storms:
	python -B src/get_storms.py

storm_visuals:
	python -B src/storm_visuals.py

all_avg_visual:
	python -B src/compare_locations_monthly.py

regplots:
	python -B src/regplot_monthly.py

# disabled for now as we have renamed files to include station names
# make command '' will download all the data and save to disk for all stations
# and data products
# raw_data/noaa_air_temperature_all.csv: data
# 	python -B src/download_noaa_tides_data.py air_temperature

# raw_data/noaa_water_temperature_all.csv: data
# 	python -B src/download_noaa_tides_data.py water_temperature

# raw_data/noaa_water_level_all.csv: data
# 	python -B src/download_noaa_tides_data.py water_level

# raw_data/noaa_hourly_height_all.csv: data
# 	python -B src/download_noaa_tides_data.py hourly_height

clean_demo:
	rm -f data/noaa_water_level_avg_month_start_1996_8418150.csv
	rm -f data/nooa_temps_avg_month_start_2009_8418150.csv
	rm -f data/noaa_water_level_diff_avg_month_start_1910_8418150.csv

clean_tides_visuals_imgs:
	rm -f figs/avg_monthly_temps_alltime_8410140.png
	rm -f figs/avg_monthly_temps_alltime_8411060.png
	rm -f figs/avg_monthly_temps_alltime_8413320.png
	rm -f figs/avg_monthly_temps_alltime_8418150.png
	rm -f figs/avg_monthly_temps_alltime_8419870.png
	rm -f figs/avg_monthly_waterlvls_alltime_8410140.png
	rm -f figs/avg_monthly_waterlvls_alltime_8411060.png
	rm -f figs/avg_monthly_waterlvls_alltime_8413320.png
	rm -f figs/avg_monthly_waterlvls_alltime_8418150.png
	rm -f figs/avg_monthly_waterlvls_alltime_8419870.png
	rm -f figs/avg_monthly_waterlvls_diff_alltime_8410140.png
	rm -f figs/avg_monthly_waterlvls_diff_alltime_8411060.png
	rm -f figs/avg_monthly_waterlvls_diff_alltime_8413320.png
	rm -f figs/avg_monthly_waterlvls_diff_alltime_8418150.png
	rm -f figs/avg_monthly_waterlvls_diff_alltime_8419870.png
	rm -f figs/eda_8410140.png
	rm -f figs/eda_8411060.png
	rm -f figs/eda_8413320.png
	rm -f figs/eda_8418150.png
	rm -f figs/eda_8419870.png
	rm -f figs/pred_vs_observed_waterlvls_week_8410140.png
	rm -f figs/pred_vs_observed_waterlvls_week_8411060.png
	rm -f figs/pred_vs_observed_waterlvls_week_8413320.png
	rm -f figs/pred_vs_observed_waterlvls_week_8418150.png
	rm -f figs/pred_vs_observed_waterlvls_week_8419870.png

rm_portland_clean:
	rm -f data/*8418150_clean.csv

rm_eastport_clean:
	rm -f data/*8410140_clean.csv

rm_cfw_clean:
	rm -f data/*8411060_clean.csv

rm_si_clean:
	rm -f data/*8419870_clean.csv

rm_bh_clean:
	rm -f data/*8413320_clean.csv

rm_clean_data:
	rm -f data/*clean.csv

clean:
	find data ! -name '*clean.csv' -type f -exec rm -f {} +
	rm -f figs/*

clean_data:
	find data ! -name '*clean.csv' -type f -exec rm -f {} +

data:
	mkdir -p data

clean_raw_data:
	rm -f raw_data/*

raw_data:
	mkdir -p raw_data

eda: clean_eda figs/eda.png

figs/eda.png: figs
	python -B src/eda.py

figs:
	mkdir -p figs

clean_eda:
	rm -f figs/eda.png
	rm -f figs/eda_8418150.png

#sets up the conda environment ds5110_fall2023_team_8
config_conda_env:	
	conda create -n ds5110_fall2023_team_8 -y
	conda install -n ds5110_fall2023_team_8 -c conda-forge numpy=1.26.0 -y
	conda install -n ds5110_fall2023_team_8 -c conda-forge pandas=2.1.1 -y
	conda install -n ds5110_fall2023_team_8 -c conda-forge matplotlib=3.8.0 -y
	conda install -n ds5110_fall2023_team_8 -c conda-forge seaborn=0.13.0 -y
	conda install -n ds5110_fall2023_team_8 -c conda-forge scikit-learn=1.3.2 -y
	conda install -n ds5110_fall2023_team_8 -c conda-forge requests=2.31.0 -y
	conda env list
	@echo "Switch to conda env with:"
	@echo "conda activate ds5110_fall2023_team_8"

#exports the conda env ds5110_fall2023_team_8 (requires `yq` installed)
environment.yml:
	conda env export -n ds5110_fall2023_team_8 --from-history > environment.yml
	yq e 'del(."prefix")' -i environment.yml

#deletes the conda env ds5110_fall2023_team_8
delete_conda_env:
	conda remove -n ds5110_fall2023_team_8 --all -y
	conda env list

#creates default .gitignore
.gitignore:
	curl -L https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore -o ".gitignore"
	@echo -e "\ndata/\n" >> .gitignore
