# Tides Data Download

The total tides data download produces 20 csv files amounting to approximately 560 MB. When run in sequence this will take approximately <span style="color:red">3 hours and 15 mins</span>.

```bash
# Use with caution! The clean data is already available in the repo and this is not required to be run
# This command will first clear the clean data files out,
# then will download all available data for each data product for each Maine station
make download_all_noaa_tides_data
```

|File|Content|Data Start Year|Station|Approx. Size (MB)|Approx. Download Duration (min)|
|----|-------|---------------|-------|-----------------|-------------------------------|
|data/noaa_air_temperature_8410140_clean.csv  |Clean 6-minute interval `air_temperature` data	|1991|[8410140 Eastport](https://tidesandcurrents.noaa.gov/inventory.html?id=8410140)			|32 |11.5|
|data/noaa_air_temperature_8411060_clean.csv  |Clean 6-minute interval `air_temperature` data	|2010|[8411060 Cutler Farris Wharf](https://tidesandcurrents.noaa.gov/inventory.html?id=8411060)|24 |6.5|
|data/noaa_air_temperature_8413320_clean.csv  |Clean 6-minute interval `air_temperature` data	|2008|[8413320 Bar Harbor](https://tidesandcurrents.noaa.gov/inventory.html?id=8413320)			|28 |7|
|data/noaa_air_temperature_8418150_clean.csv  |Clean 6-minute interval `air_temperature` data	|2009|[8418150 Portland](https://tidesandcurrents.noaa.gov/inventory.html?id=8418150)			|26 |5|
|data/noaa_air_temperature_8419870_clean.csv  |Clean 6-minute interval `air_temperature` data	|2021|[8419870 Seavey Island](https://tidesandcurrents.noaa.gov/inventory.html?id=8419870)		|3.5|1|
|data/noaa_hourly_height_8410140_clean.csv    |Clean hourly interval `water_level` data			|1929|[8410140 Eastport](https://tidesandcurrents.noaa.gov/inventory.html?id=8410140)			|22 |10|
|data/noaa_hourly_height_8411060_clean.csv    |Clean hourly interval `water_level` data			|2010|[8411060 Cutler Farris Wharf](https://tidesandcurrents.noaa.gov/inventory.html?id=8411060)|3.2|2.5|
|data/noaa_hourly_height_8413320_clean.csv    |Clean hourly interval `water_level` data			|1947|[8413320 Bar Harbor](https://tidesandcurrents.noaa.gov/inventory.html?id=8413320)			|18 |9|
|data/noaa_hourly_height_8418150_clean.csv    |Clean hourly interval `water_level` data			|1910|[8418150 Portland](https://tidesandcurrents.noaa.gov/inventory.html?id=8418150)			|27 |5.5|
|data/noaa_hourly_height_8419870_clean.csv    |Clean hourly interval `water_level` data			|1926|[8419870 Seavey Island](https://tidesandcurrents.noaa.gov/inventory.html?id=8419870)		|14 |10.5|
|data/noaa_water_level_8410140_clean.csv      |Clean 6-minute interval `water_level` data		|1996|[8410140 Eastport](https://tidesandcurrents.noaa.gov/inventory.html?id=8410140)			|68 |21|
|data/noaa_water_level_8411060_clean.csv      |Clean 6-minute interval `water_level` data		|2010|[8411060 Cutler Farris Wharf](https://tidesandcurrents.noaa.gov/inventory.html?id=8411060)|32 |16|
|data/noaa_water_level_8413320_clean.csv      |Clean 6-minute interval `water_level` data		|1997|[8413320 Bar Harbor](https://tidesandcurrents.noaa.gov/inventory.html?id=8413320)			|57 |20.5|
|data/noaa_water_level_8418150_clean.csv      |Clean 6-minute interval `water_level` data		|1996|[8418150 Portland](https://tidesandcurrents.noaa.gov/inventory.html?id=8418150)			|67 |15.5|
|data/noaa_water_level_8419870_clean.csv      |Clean 6-minute interval `water_level` data		|1998|[8419870 Seavey Island](https://tidesandcurrents.noaa.gov/inventory.html?id=8419870)		|12 |17.5|
|data/noaa_water_temperature_8410140_clean.csv|Clean 6-minute interval `water_temperature` data	|1995|[8410140 Eastport](https://tidesandcurrents.noaa.gov/inventory.html?id=8410140)			|29 |10|
|data/noaa_water_temperature_8411060_clean.csv|Clean 6-minute interval `water_temperature` data	|2010|[8411060 Cutler Farris Wharf](https://tidesandcurrents.noaa.gov/inventory.html?id=8411060)|23 |5|
|data/noaa_water_temperature_8413320_clean.csv|Clean 6-minute interval `water_temperature` data	|1999|[8413320 Bar Harbor](https://tidesandcurrents.noaa.gov/inventory.html?id=8413320)			|28 |8.5|
|data/noaa_water_temperature_8418150_clean.csv|Clean 6-minute interval `water_temperature` data	|1997|[8418150 Portland](https://tidesandcurrents.noaa.gov/inventory.html?id=8418150)			|40 |9|
|data/noaa_water_temperature_8419870_clean.csv|Clean 6-minute interval `water_temperature` data	|2021|[8419870 Seavey Island](https://tidesandcurrents.noaa.gov/inventory.html?id=8419870)		|3.4|1|