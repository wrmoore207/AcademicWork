import pandas as pd
from os.path import isfile
from location_class import Location
from helpers import save_csv, parse_year
from load_noaa_tides_data import load_noaa_tides_data_product

def findDifference(data):
    data["Difference"] = data["Water Level"].sub(data["Prediction"])

    return data

def find_waterlvl_diff_avg_month(location):
    datafile = f'data/noaa_water_level_diff_avg_month_start_{parse_year(location.start_date)}_{location.station_id}.csv'

    if isfile(datafile):
        data = pd.read_csv(datafile)
    else:
        data = load_noaa_tides_data_product(location)
        data = findDifference(data)

        # average by month
        data['Date Time'] = pd.to_datetime(data['Date Time'], format='%Y-%m-%d %H:%M')
        data = data[['Date Time', 'Water Level', 'Prediction', 'Difference']]
        data = data.groupby(pd.PeriodIndex(data['Date Time'], freq='M')).mean()

        data.index.names = ['Month']

        data = data.drop(columns=['Date Time', 'Water Level', 'Prediction'])
        # print("find_waterlvl_diff_avg_month() df:\n{}".format(data))
        save_csv(data, datafile, True)

    return data

def averageData(data):
    df = pd.DataFrame()
    df["Date"] = [data["Date Time"].iloc[0][:7]]
    df["Avg Water Level"] = [data["Water Level"].mean()]
    df["Avg Prediction"] = [data["Prediction"].mean()]
    print(df)
    return df

def average_by_month(location):
    datafile = f'data/noaa_water_level_avg_month_start_{parse_year(location.start_date)}_{location.station_id}.csv'

    if isfile(datafile):
        df = pd.read_csv(datafile)
    else:
        df = load_noaa_tides_data_product(location, 'water_level')

        df['Date Time'] = pd.to_datetime(df['Date Time'], format='%Y-%m-%d %H:%M')
        df = df[['Date Time', 'Water Level', 'Prediction']]
        df = df.groupby(pd.PeriodIndex(df['Date Time'], freq='M')).mean()

        df.index.names = ['Month']

        # print("average_by_month() df:\n{}".format(df))
        save_csv(df, datafile, True)

    return df

# saves csv of avg air and water temps by month
def avg_temps_by_month(location):
    datafile = f"data/nooa_temps_avg_month_start_{format(parse_year(location.start_date))}_{location.station_id}.csv"

    if isfile(datafile):
        temps = pd.read_csv(datafile)
    else:
        watertemp = load_noaa_tides_data_product(location, 'water_temperature')
        airtemp = load_noaa_tides_data_product(location, 'air_temperature')

        # merges the 6-minute interval data for Water Temperatures and
        # Air Temperatures
        temps = watertemp.copy().join(airtemp[['Air Temp']].copy(), how='inner')

        temps[['Year-Month', 'DoM']] = temps['Date'].str.rsplit('-', expand=True, n=1)
        
        temps = temps.groupby(by='Year-Month', as_index=False)[['Air Temp', 'Water Temp']].mean()

        save_csv(temps, datafile, True)

    # print(temps)
    # print(list(temps.columns.values))

    return temps


#remove comment and run data_editing to test average by month
#average_by_month()