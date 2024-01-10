# Load the NOAA Tides and Currents Data

## load_noaa_tides_data.py Usage


The program will load the "clean" data files checked into the repo. The program will select data for the date range specified in the `Location` object and return only that data in the DataFrame.

* If the clean data is not already on disk when you try to load the data, the program will make a series of calls to the NOAA webservice first depending on the date range specified and the parameter `use_all_time_data`. If `use_all_time_data` is `False` (default) then data will be pulled from the beginning of the year for start year specified in the `Location` object up to the end of the current year. By default, the raw data is not saved to disk. Upon loading the data, a csv of "cleaned" data is saved to the disk. This will be used by the program going forward.

To load one of the data products:

```python
from load_noaa_tides_data import load_noaa_tides_data_product
from location_class import setup_station_by_data_product

location = setup_station_by_data_product('portland', 'water_level')
df = load_noaa_tides_data_product(location, "water_level", use_all_time_data=False)

print(df.head())
```

```text
                            Date Time        Date   Time  Water Level  	Prediction 
Date Time                                                                          
2023-01-01 00:00:00  2023-01-01 00:00  2023-01-01  00:00        8.726        8.366 
2023-01-01 00:06:00  2023-01-01 00:06  2023-01-01  00:06        8.617        8.271 
2023-01-01 00:12:00  2023-01-01 00:12  2023-01-01  00:12        8.555        8.166 
2023-01-01 00:18:00  2023-01-01 00:18  2023-01-01  00:18        8.466        8.051 
2023-01-01 00:24:00  2023-01-01 00:24  2023-01-01  00:24        8.384        7.927
```
