"""
Graphs water levels, air temps, and water temps for the Portland, ME
station.

DS5110 Fall 2023 Project Team 8 SDG

2023-11-09

:Authors:
Lukas Hernandez <hernandez.lu@northeastern.edu>
Johnathan Green <green.john@northeastern.edu>
Ryan Moore <moore.will@northeastern.edu>

"""

from load_noaa_tides_data import load_noaa_tides_data_product
from graphing import graph_month_avg_temps, graph_change, graph_week, \
    graph_avg_water_by_month, graph_diff_waterlvl_obs_pred_avg_month
from data_editing import average_by_month, avg_temps_by_month, \
    find_waterlvl_diff_avg_month, averageData
from location_class import setup_station_by_start_year, \
    setup_station_by_data_product, setup_station_one_week

# makes graphs of eda figure for all maine stations
def make_eda_by_station(station_name, display=False):
    location = setup_station_one_week(station_name)
    
    if display:
        imagefile = None
    else:
        imagefile = f'figs/eda_{location.station_id}.png'
    
    graph_week(location, imagefile)

# makes graph of difference in observed and predicted water levels
# over one week. By default, just saves the image. If display == True,
# image will be displayed and not saved.
def make_graph_pred_vs_obs_week(location, display=False):
    data = load_noaa_tides_data_product(location)

    if display:
        imagefile = None
        averageData(data)
    else:
        imagefile = f'figs/pred_vs_observed_waterlvls_week_{location.station_id}.png'
    
    graph_change(data, location, imagefile)

# makes graph of difference in observed and predicted water levels
# since 1910 averaged by month.
def make_graph_pred_vs_obs_avg_month(location, display=False):
    data = find_waterlvl_diff_avg_month(location)

    if display:
        imagefile = None
    else:
        imagefile = f"figs/avg_monthly_waterlvls_diff_alltime_{location.station_id}.png"
    
    graph_diff_waterlvl_obs_pred_avg_month(data, location, imagefile)

# makes graph of average water levels by month
def make_graph_avg_water_by_month(location, display=False):
    df = average_by_month(location)

    if display:
        imagefile = None
    else:
        imagefile = f"figs/avg_monthly_waterlvls_alltime_{location.station_id}.png"
    
    graph_avg_water_by_month(df, location, imagefile)

# makes graph of the average monthly water and air temps since 2009
def make_graph_avg_monthly_temps(location, display=False):
    temps = avg_temps_by_month(location)
 
    print(f"make_graph_avg_monthly_temps temps:\n{temps}")
    if display:
        imagefile = None
    else:
        imagefile = f'figs/avg_monthly_temps_alltime_{location.station_id}.png'
 
    # shows the trend over time
    graph_month_avg_temps(temps, location, imagefile)

def main():
    # EDA figure over all stations
    for station in ['portland', 'eastport', 'cfw', 'si', 'bh']:
        make_eda_by_station(station)

        # Portland - predicted water levels vs observed water levels for one week
        #station = 'portland'
        location = setup_station_one_week(station)

        make_graph_pred_vs_obs_week(location)

        location = setup_station_by_data_product(station, "hourly_height")
        make_graph_pred_vs_obs_avg_month(location)

        if station == 'portland':
            make_graph_pred_vs_obs_avg_month(location, True)

        location = setup_station_by_data_product(station, 'water_level')
        make_graph_avg_water_by_month(location)

        if station == 'portland':
            make_graph_avg_water_by_month(location, True)

    location = setup_station_by_start_year("portland", "2009")
    make_graph_avg_monthly_temps(location)

    location = setup_station_by_start_year("eastport", "1995")
    make_graph_avg_monthly_temps(location)
    
    location = setup_station_by_start_year("cfw", "2010")
    make_graph_avg_monthly_temps(location)
    
    location = setup_station_by_start_year("si", "2021")
    make_graph_avg_monthly_temps(location)
    
    location = setup_station_by_start_year("bh", "2008")
    make_graph_avg_monthly_temps(location)

if __name__ == '__main__':
    main()
