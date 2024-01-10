"""
Loads NOAA tides data to Pandas DataFrames.
Creates a local copy of cleaned up data as
csv if not already on disk.

DS5110 Fall 2023 Project Team 8 SDG

2023-11-07

:Authors:
Lukas Hernandez <hernandez.lu@northeastern.edu>
Johnathan Green <green.john@northeastern.edu>
Ryan Moore <moore.will@northeastern.edu>

"""

import os
import urllib.parse
import pandas as pd
import time
from location_class import Location
from datetime import datetime
from helpers import parse_year, save_csv, calc_last_day_of_month

def load_noaa_tides_data_product(location=None, product='hourly_height', use_all_time_data=False):
    """
    Loads the specified NOAA tides data product for the Portland, ME station as a Pandas DataFrame.
    Data is cleaned up after loading. Cleaned data is saved to disk.
    Downloads the raw data first if specified.

    The loaded data set has observations in the specified date range

    Parameters
    ----------
    start_date : str, optional
      Start date of data retrieval in format `YYYYMMDD`

    end_date :
      End date of data retrieval in format `YYYYMMDD`

    product : str, optional
      `water_level`, `air_temperature`, `water_temperature`
      available in 6-minute intervals for 1-month period data-length.
      `hourly_height` available for 1-year period data-length

    use_all_time_data : bool, optional
      Specifies if the data for all time should be used to create the data set.
      If set to `True`, this may result in long load times if the data has not been
      downloaded ahead of time with `download_noaa_tides_data.py`
    
    Data range
    ----------
      * Portland: https://tidesandcurrents.noaa.gov/inventory.html?id=8418150
      * Eastport: https://tidesandcurrents.noaa.gov/inventory.html?id=8410140
      * Cutler Farris Wharf: https://tidesandcurrents.noaa.gov/inventory.html?id=8411060
      * Seavey Island: https://tidesandcurrents.noaa.gov/inventory.html?id=8419870
      * Bar Harbor: https://tidesandcurrents.noaa.gov/inventory.html?id=8413320
    """

    # default dates and location: May 2023 for Portland, ME
    if location is None:
        location = Location("20230501", "20230531", "8418150")

    input_start_date = location.start_date
    input_end_date = location.end_date
    print(f"location: {location}")
    data_file = f"data/noaa_{product}_{location.station_id}_clean.csv"

    if os.path.isfile(data_file):
        print("Found file for '{}' clean data for all time for station {} {}. "
              "Loading data for dates {} to {}".format(
                  product, location.station_id, location.get_station_name(),
                  location.start_date, location.end_date))
    elif use_all_time_data:
        print("Retrieving '{}' clean data for all time for station {} {}. "
              "Loading data for dates {} to {}".format(
                  product, location.station_id, location.get_station_name(),
                  location.start_date, location.end_date))
    else:
        print("Loading '{}' clean data for station {} {} for dates {} "
          "to {}".format(product, location.station_id, location.get_station_name(),
          location.start_date, location.end_date))
        data_file = f"data/noaa_{product}_start_{parse_year(location.start_date)}_{location.station_id}_clean.csv"

    # save the cleaned up data set if necessary
    if not os.path.isfile(data_file):
        print(f"Clean data file for product '{product}' not found, writing as '{data_file}'")
        df = load_noaa_tides_data_product_raw(location, product, use_all_time_data)

        # print(f"before make_tides_data_tidy df:\n{df}")
        # Tidy up the Tides data
        df = make_tides_data_tidy(df, product)
        # print(f"after make_tides_data_tidy df:\n{df}")

        # save the cleaned up data to disk
        save_csv(df, data_file)
    else:
        df = pd.read_csv(data_file)

    # Split "Date Time" to two columns "Date" and "Time". Original Date Time
    # remains in dataset.
    df = split_date_time_col(df)

    # set the date & time as the index
    set_datetime_index(df)
    # print(f"Date index: {df.index}")


    # get data by input date range. Reset the location's date gets
    # since it gets modified by the data pull
    # print(f"before select_by_dates df:\n{df}")
    location.start_date = input_start_date
    location.end_date = input_end_date
    # print(f"location: {location}")
    df = select_by_dates(df, location)
    # print(f"after select_by_dates df:\n{df}")

    print(f"load_noaa_tides_data_product() df:\n{df}")
    return df

def load_noaa_tides_data_all_products(location, use_all_time_data=False):
    """
    Loads a data frame for each data product
    """
    if location is None:
       location = Location("20230501", "20230531", "8418150")

    products = ['air_temperature', 'water_temperature',
                'hourly_height', 'water_level']

    df_hrheight = load_noaa_tides_data_product(start_date=location.start_date,
                      end_date=location.end_date, product=products[2],
                      use_all_time_data=use_all_time_data)
    # print(f"df_hrheight:\n{df_hrheight.tail()}")

    df_waterlvl = load_noaa_tides_data_product(start_date=location.start_date,
                      end_date=location.end_date, product=products[3],
                      use_all_time_data=use_all_time_data)
    # print(f"df_waterlvl:\n{df_waterlvl.tail()}")

    df_watertemp = load_noaa_tides_data_product(start_date=location.start_date,
                      end_date=location.end_date, product=products[1],
                      use_all_time_data=use_all_time_data)
    # print(f"df_watertemp:\n{df_watertemp.tail()}")

    df_airtemp = load_noaa_tides_data_product(start_date=location.start_date,
                      end_date=location.end_date, product=products[0],
                      use_all_time_data=use_all_time_data)
    # print(f"df_airtemp:\n{df_airtemp.tail()}")

    return df_hrheight, df_waterlvl, df_watertemp, df_airtemp

def load_noaa_tides_data_product_raw(location, product='hourly_height', use_all_time_data=False, save_raw_data=False):
    """
    Loads the specified NOAA tides data product raw data as a Pandas DataFrame.
    Downloads the raw data first if necessary.
    """

    data_file = f"raw_data/noaa_{product}_{location.station_id}_all.csv"

    # use the pre-downloaded data if it's already on disk
    if os.path.isfile(data_file) or use_all_time_data:
        print(f"Loading '{product}' raw data for station {location.station_id} {location.get_station_name()} from all time")
        download_start_date = None
    else:
      print(f"Loading '{product}' raw data for station {location.station_id} {location.get_station_name()} starting from {location.start_date}")
      download_start_date = location.start_date
      data_file = f"raw_data/noaa_{product}_start_{parse_year(location.start_date)}_{location.station_id}.csv"

    location.start_date = download_start_date
    # download data set if necessary
    if not os.path.isfile(data_file):
        if save_raw_data:
            print(f"data file for product '{product}' for station {location.station_id} {location.get_station_name()} not found, downloading as '{data_file}'")
            df = download_all_data(product, data_file, location)
        else:
            df = get_all_data(product, location)
    else:
        df = pd.read_csv(data_file)

    return df

def download_all_data(product, location, filename=None):
    """
    Downloads all available NOAA tides data for the specified data product and
    saves it to disk as a csv
    """
    df = get_all_data(product, location)

    save_csv(df, filename)

    # get file size in MB, os returns in bytes.
    file_size = os.path.getsize(filename) / 1024 / 1024

    print("Downloaded '{}' ({:.2f} MB)"
    .format(filename, file_size))

    return df

def get_all_data(product, location):
    """
    Gets all NOAA data for specified product
    """
    start_time = datetime.now() # track data pull duration
    end_year = "2023"

    # if (product == 'hourly_height'):
    #   # 'hourly_height' data begins year 1910
    #   start_year = "1910"
    # elif (product == 'water_level'):
    #   # 'water_level' data begins year 1996
    #   start_year = "1996"
    # elif (product == 'air_temperature'):
    #   # 'air_temperature' data begins year 2009
    #   start_year = "2009"
    # elif (product == 'water_temperature'):
    #   # 'water_temperature' data begins year 1997
    #   start_year = "1997"

    # set start of data pull based on need
    if location.start_date is not None:
      start_year = parse_year(location.start_date)
    else:
       start_year = location.get_station_data_start_year(product)
    
    # set end of data pull based on need
    if location.end_date != None:
      end_year = parse_year(location.end_date)
    

    df = get_multi_year_data(start_year, end_year, product, location)

    # print(f"all 'hourly_height' data df.shape: {df.shape}")
    # print(f"all 'hourly_height' data df.columns.values: {df.columns.values}")
    
    # track data pull duration
    end_time = datetime.now()
    duration = end_time - start_time

    print(f"Got all data for product '{product}' station {location.station_id} years {start_year} to {end_year} in {duration}")
    return df

def drop_unverified_data(df):
    """
    Removes water_level data that hasn't been verified yet
    """

    # for water_level drop unverified (preliminary) data
    df = df.loc[~(df[' Quality '] == 'p')]

    # drop ' Quality ' column since all rows are verified
    df = df.drop(columns=' Quality ')

    return df

def rename_columns(df, product):
    """
    Renames columns for the specified NOAA Tides data product
    to make them easier to work with.
    """

    new_cols = None
    if product == 'air_temperature':
      new_cols={ ' Air Temperature': 'Air Temp',
                  ' X': 'X',
                  ' N': 'N',
                  ' R ': 'R'
                }
    elif product == 'water_temperature':
      new_cols={ ' Water Temperature': 'Water Temp',
                ' X': 'X',
                ' N': 'N',
                ' R ': 'R'
              }
    elif product == 'hourly_height':
      new_cols={ ' Water Level': 'Water Level',
                ' Sigma': 'Sigma',
                ' I': 'I',
                ' L ': 'L',
                ' Prediction': 'Prediction'
              }
    elif product == 'water_level':
      new_cols={ ' Water Level': 'Water Level',
                ' Sigma': 'Sigma',
                ' O or I (for verified)': 'I',
                ' F': 'F',
                ' R': 'R',
                ' L': 'L',
                ' Prediction': 'Prediction'
              }

    if new_cols:
      df = df.rename(columns=new_cols)

    return df

def drop_unused_columns(df, product):
    """
    Removes columns we don't intend to use based on the NOAA data product type
    """
    drop_cols = []
    if product == 'water_level':
        drop_cols = ['Sigma', 'I', 'F', 'R', 'L']
    elif product == 'hourly_height':
        drop_cols = ['Sigma', 'I', 'L']
    elif product in ['air_temperature', 'water_temperature']:
        drop_cols = ['X', 'N', 'R']
    
    # print(f"Before dropping columns:\n{df.head()}\n")

    df = df.copy().drop(columns=drop_cols)
    # print(f"After dropping columns:\n{df.head()}\n")

    return df

def split_date_time_col(df):
    """
    Split 'Date Time' column to two columns
    """

    temp = df.copy()
    temp[['Date', 'Time']] = df['Date Time'].str.split(' ', expand=True)

    # print(f"split_date_time_col temp:\n{temp}")
    # re-order the columns and make new "Date" and "Time" columns second and
    # third after "Date Time"
    df_cols = list(temp.columns.values)
    df_cols.insert(1, df_cols.pop(-2))
    df_cols.insert(2, df_cols.pop(-1))

    df = temp[df_cols]
    # print(f"split_date_time_col df:\n{df}")

    return df

def set_datetime_index(df):
    """
    Sets the dataframe index to the "Date Time" column. Allows slicing
    the df by date range as in: `df = df["20230501":"20230531"]
    """
    df.index = pd.to_datetime(df['Date Time'].copy())

def make_tides_data_tidy(df, product):
    """
    Removes missing data, renames columns based on product, splits "Date Time"
    to two columns.
    """
    # remove any missing data
    df = df.dropna()

    # use only verified data for 'water_level'
    if product == 'water_level':
      df = drop_unverified_data(df)

    # rename columns based on data product
    df = rename_columns(df, product)

    df = drop_unused_columns(df, product)

    return df

def select_by_dates(df, location):
    """
    Returns a slice of the dataframe for given date range
    """

    temp = df.loc[location.start_date:location.end_date]

    # print(f"select_by_dates temp:\n{temp}")
    return temp

def buildUrls(product, datum, location):
    """
    Builds the URL(s) to call the NOAA web service for Tides and Water Levels
    data

    Returns
    ------
    queryUrl - Encoded URL string for fetching NOAA data

    predictQueryUrl - Encoded URL string for fetching NOAA predictions for
    corresponding water product data
    """

    # force correct case for string parameters
    product = product.lower()
    datum = datum.upper()

    url = 'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?'

    params = {
        # an “identifier” in automated activity / error logs that allows us
        # (NOAA) to identify your query from others.
        'application': 'DS5110_Fall2023_ProjectTeam8',
        'product': product,
        'station': location.station_id,
        'begin_date': location.start_date,
        'end_date': location.end_date,
        'time_zone': "GMT",
        'datum': datum,
        'units': "english",
        'format': 'csv'
    }

    queryUrl = url + urllib.parse.urlencode(params)

    # query for predictions for 'hourly_height' requires additional
    # parameter 'interval'
    if(product == 'hourly_height'):
      params['interval'] = 'h'

    # return a query for predictions as well for products
    # 'water_level' and 'hourly_height'
    if(product in ['hourly_height', 'water_level']):
      params['product'] = 'predictions'
      predictQueryUrl = url + urllib.parse.urlencode(params)
    else:
      predictQueryUrl = None

    return queryUrl, predictQueryUrl

def getNoaaTidesData(location, product="hourly_height",
                    datum="MLLW"):
    """
    Retrieve NOAA Tides and Water Levels data as specified in the parameters

    Parameters
    ----------
    Params reference: https://api.tidesandcurrents.noaa.gov/api/prod/
    location : Location, class for station and date parameters
      station : str, optional
        The station where tide and water level measurements were taken
        (default is 8418150 for Portland, ME, USA).

      start_date :
        Start date of data retrieval

      end_date :
        End date of data retrieval

    product : str, optional
      Type of data:
        'water_level', 'air_temperature', 'water_temperature'
        available in 6-minute intervals for 1-month period data-length.
        'hourly_height' available for 1-year period data-length

      Data range:
        'water_level' is available starting 1996
        'hourly_height' is available starting 1910
        'air_temperature' is available starting 2009
        'water_temperature' is available starting 1997
        See data inventory for station:
        https://tidesandcurrents.noaa.gov/inventory.html?id=8418150

    datum : str, optional
      see params reference above
    """

    query_url, predict_url = buildUrls(product, location=location,
                                       datum=datum)

    # print(f"query_url: {query_url}")
    df = None
    attempts = 0
    
    while df is None and attempts < 3:
      try:
        if (predict_url != None):
          # print(f"predict_url: {predict_url}")
          # predictions are only available on water level / tide data,
          # create a data frame with the measured and predicted water levels
          df = pd.merge(pd.read_csv(query_url), pd.read_csv(predict_url),
                        on='Date Time')
        else:
          # create a data frame with the measured air or water temps
          df = pd.read_csv(query_url)
      except Exception as e:
          print("Error retrieving data from NOAA Tides webservice on attempt {}. query_url='{}'"
                ", predict_url='{}'\n{}\n{}".format((attempts + 1), query_url, predict_url, type(e), e))

      attempts += 1
      time.sleep(1)

    # print(f"getNoaaTidesData df:\n{df}")
    return df

def get_month_data(location, start_year="2023", start_month="05", start_day="01",
                   product="water_level"):
    """
      Retrieve NOAA Tides and Water Levels data as specified in the parameters
      Use for data products: 'water_level', 'air_temperature',
       'water_temperature'

      Parameters
      ----------
      start_year: str, optional
        Year of data to pull

      start_month: str, optional
        Month of data to pull

      start_day: str, optional
        Day of data to pull

      product: str, optional
        Type of data to pull. See getNoaaTidesData()
    """

    year_num = int(start_year)
    day_num = int(start_day)

    day_offset = calc_last_day_of_month(start_month, year_num)

    # calculate end date as a string for the period to graph
    start_date = start_year + start_month + start_day
    end_day = str(day_num + day_offset).rjust(2, '0')
    end_date = start_year + start_month + end_day

    #portland value hardcoded temporarily
    # #look here for confusion
    # portland = Location(start_date, end_date, "8418150")

    location.start_date = start_date
    location.end_date = end_date
    df = getNoaaTidesData(location,
                            product=product)
    
    # print(f"get_month_data df:\n{df}")
    return df

def get_year_data(year, product, location):
    """
    Retrieves a year's worth of NOAA data for the specified product

    Parameters
    ----------
    year: str, optional
      Year of data to pull

    product: str, optional
      Type of data to pull. See getNoaaTidesData()
    """

    # initial variables for start and end date strings for the NOAA calls
    month = "01"
    day = "01"

    # data length is limited to one month for: 'water_level', 'air_temperature',
    # and 'water_temperature' since they have data in six-minute intervals
    if (product != 'hourly_height'):

      # print(f"yyyymmdd: {year + month + day}")
      df = get_month_data(location, start_year=year, start_month=month, start_day=day,
                          product=product)
      # print(f"df.shape: {df.shape}")

      month_num = int(month)
      while (month_num < 12):
          month = f"0{month_num + 1}" if month_num < 9 else f"{month_num + 1}"
          month_num = int(month)
          # print(f"yyyymmdd: {year + month + day}")
          temp = get_month_data(location, start_year=year, start_month=month,
                                start_day=day, product=product)
          # print(f"temp.shape: {temp.shape}")

          df = pd.concat([df, temp], axis=0)
          # print(f"df.shape: {df.shape}")
    else:
      # last day of the year will always be December 31
      # no special calculations here
      end_month = "12"
      end_day = "31"
      # data length is limited to one year for 'hourly_height'
      # get a year's worth of 'hourly_height' data with one call
      location.start_date = year + month + day
      location.end_date = year + end_month + end_day
      df = getNoaaTidesData(location, product=product)
      # print(f"df.shape: {df.shape}")

    # print(f"get_year_data, df.shape: {df.shape}")
    # print(f"get_year_data df:\n{df}")
    print(f"Got year of data for product '{product}' station {location.station_id} year {year}")
    return df

def get_multi_year_data(start_year, end_year, product, location):
    """
    Pulls data for multiple years, one year at a time.
    """

    print(f"Getting '{product}' data for station {location.station_id} {location.get_station_name()} for years: {start_year} to { end_year}...")

    df = pd.DataFrame()

    # range does not include the 'stop' number in the values it returns,
    # increment 'stop' by 1 to get all the data we want
    for year in range(int(start_year), int(end_year) + 1):
      #print(f"Getting '{product}' data for year: {year}")
      temp = get_year_data(str(year), product, location)
      # print(f"get_multi_year_data temp.shape: {temp.shape}")
      # print(f"get_multi_year_data temp.columns.values: {temp.columns.values}")

      df = pd.concat([df, temp])

    # print(f"get_multi_year_data df:\n{df}")
    print(f"Got data for years {start_year} to {end_year}")
    return df
