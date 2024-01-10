"""
Downloads all NOAA data to disk for specified product and station.
Requires 'raw_data' and 'data' folders to exist.
Saves in clean or raw format depending on input options.

DS5110 Fall 2023 Project Team 8 SDG

2023-11-07

:Authors:
Lukas Hernandez <hernandez.lu@northeastern.edu>
Johnathan Green <green.john@northeastern.edu>
Ryan Moore <moore.will@northeastern.edu>

"""

import argparse
from load_noaa_tides_data import load_noaa_tides_data_product_raw, \
    load_noaa_tides_data_product
from location_class import Location

# downloads all time data for all products or single specified product
# for the station specified
def download_data_product(product, location, data_format):
    if product in products:
        print(f"downloading data for '{product}' for station {location.station_id} {location.get_station_name()}")
        
        save_by_data_format(location, product, data_format)
    elif product == 'all':
        print(f"downloading all data products for station {location.station_id} {location.get_station_name()}")

        # download each data product individually
        for p in products:
            temp_loc = Location(location.start_date, location.end_date, location.station_id)
            save_by_data_format(temp_loc, p, data_format)
    else:
        print(f"unsupported product: '{product}'. not downloading")

# saves raw, clean or both
def save_by_data_format(location, product, data_format):
    # save raw data first, saving clean data will use the raw file if available
    if data_format in ['raw', 'all']:
        print(f"saving raw {product} data for {location.get_station_name()} {location}")
        load_noaa_tides_data_product_raw(location, product, use_all_time_data=True, save_raw_data=True)
    if data_format in ['clean', 'all']:
        print(f"saving clean {product} data for {location.get_station_name()} {location}")
        load_noaa_tides_data_product(location, product, use_all_time_data=True)

products = ['hourly_height', 'water_level', 
                    'air_temperature', 'water_temperature']
product_choices = products.copy()
product_choices.append('all')
# print(f"products: {products}")
print(f"product choices: {product_choices}")

# portland 8418150 should be first in the list. It will be used as default station
station_ids = ['8418150', '8410140', '8411060', '8419870', '8413320']
station_id_choices = station_ids.copy()
station_id_choices.append('all')
# print(f"station_ids: {station_ids}")
print(f"station_id choices: {station_id_choices}")

data_formats = ['clean', 'raw', 'all']

parser = argparse.ArgumentParser()
parser.add_argument("product", help="enter NOAA tides data product to download",
                    choices=product_choices)
parser.add_argument("station_id", help="enter station_id for NOAA tides data to download",
                    choices=station_id_choices)
parser.add_argument("data_format", help="enter station_id for NOAA tides data to download",
                    choices=data_formats)

args = parser.parse_args()

product = args.product.lower()

if args.station_id:
    station_id = args.station_id.lower()
else:
    station_id = station_ids[0]

data_format = args.data_format.lower()

# download the data product(s) for all known stations
# or for singular input station. Does not specify dates,
# this forces the data pull to get all available data based on
# mapping in location_class
if station_id == 'all':
    for id in station_ids:
        location = Location(None, None, id)
        download_data_product(product, location, data_format)
else:
    location = Location(None, None, station_id)
    download_data_product(product, location, data_format)

