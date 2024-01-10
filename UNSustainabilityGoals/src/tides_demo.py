"""
Demonstrates some things that can be done with the data set
"""

from graphing import graph_week
from location_class import Location, setup_station_by_start_year, \
    setup_station_by_data_product, setup_station_one_week
from tides_visualizations import make_graph_pred_vs_obs_week, \
    make_graph_pred_vs_obs_avg_month, make_graph_avg_water_by_month, \
    make_graph_avg_monthly_temps

stations = ['portland', 'eastport', 'cfw', 'si', 'bh']

# graph the eda figure, measured water height * predicted
def demo_eda():
    for station in stations:
        location = setup_station_one_week(station)
        graph_week(location)

# graph difference in observed and predicted water levels
# over one week. prints the average water levels
def demo_graph_pred_vs_obs_week():
    for station in stations:
        location = setup_station_one_week(station)
        make_graph_pred_vs_obs_week(location, True)

# graph difference in observed and predicted water levels
# since 1910 averaged by month.
def demo_graph_pred_vs_obs_avg_month():
    for station in stations:
        location = setup_station_by_data_product(station, 'hourly_height')
        make_graph_pred_vs_obs_avg_month(location, True)

# graph average water levels by month since 1996
def demo_graph_avg_water_by_month():
    for station in stations:
        location = setup_station_by_data_product(station, 'water_level')
        make_graph_avg_water_by_month(location, True)

# shows the average monthly water and air temps since 2009
def demo_graph_avg_monthly_temps():
    location = setup_station_by_start_year("portland", "2009")

    make_graph_avg_monthly_temps(location, True)
    
    location = setup_station_by_start_year("eastport", "1995")

    make_graph_avg_monthly_temps(location, True)
    
    location = setup_station_by_start_year("cfw", "2010")

    make_graph_avg_monthly_temps(location, True)
    
    location = setup_station_by_start_year("si", "2021")

    make_graph_avg_monthly_temps(location, True)
    
    location = setup_station_by_start_year("bh", "2008")

    make_graph_avg_monthly_temps(location, True)

# demonstrate the progress. Comment out to disable
demo_eda()
demo_graph_pred_vs_obs_week()
demo_graph_pred_vs_obs_avg_month()
demo_graph_avg_water_by_month()
demo_graph_avg_monthly_temps()
