"""
Methods to graph the NOAA Tide and Waters Level data

DS5110 Fall 2023 Project Team 8 SDG

2023-11-09

:Authors:
Lukas Hernandez <hernandez.lu@northeastern.edu>
Johnathan Green <green.john@northeastern.edu>
Ryan Moore <moore.will@northeastern.edu>
"""

from load_noaa_tides_data import load_noaa_tides_data_product, split_date_time_col
from data_editing import findDifference
from helpers import save_or_display_graph
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from location_class import Location
from helpers import parse_year

def graph_week(location, figname=None):
    """
    Graph one week's worth of NOAA data starting at the date specified

    Parameters
    ----------

    location : Location, required
      Data Product and Start & End Dates for data pull

    figname : str, optional
      Filename to save graph as. If not specified, graph will display instead of save.
    """
    plt.clf()
    # fetch data from NOAA web service
    data = load_noaa_tides_data_product(location)

    # plot the data
    line = sns.lineplot(data, x="Date Time", y="Water Level", legend="brief", label="Actual")
    sns.lineplot(data, x="Date Time", y="Prediction", legend="brief", label="Predicted", color="red", alpha=0.6)
    for ind, label in enumerate(line.get_xticklabels()):
        if ind % 10 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)
    line.tick_params(bottom=False)
    plt.xticks(rotation=45)
    plt.xlabel("Date Time (GMT)")
    plt.ylabel("Water Level (Feet)")
    title = f"{location.get_station_name()} Tidal Water Levels (1 Week)"
    plt.title(title)
    plt.tight_layout()

    save_or_display_graph(plt, figname)

def graph_change(data, location, figname=None):
    plt.clf()
    data = findDifference(data)
    line = sns.lineplot(data, x="Date Time", y="Difference")
    for ind, label in enumerate(line.get_xticklabels()):
        if ind % 10 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)
    line.tick_params(bottom=False)
    plt.xticks(rotation=45)
    plt.ylabel("Difference in Water Level (Feet)")
    title = "Water Level (Observed - Predicted) Over One Week for {}".format(
        location.get_station_name()
        )
    plt.title(title)
    plt.tight_layout()
    
    save_or_display_graph(plt, figname)

def graph_diff_waterlvl_obs_pred_avg_month(data, location, figname=None):
    plt.clf()
    data = data.reset_index()
    # print("graph_diff_waterlvl_obs_pred_avg_month()\n{}".format(data))
    ax = sns.lineplot(data, x=data["Month"].astype(str), y="Difference")
    ax.xaxis.set_major_locator(ticker.LinearLocator(round(data.shape[0]/60)))
    ax.axhline(0, linewidth=1, c='k')
    plt.xticks(rotation=45)
    plt.ylabel("Average Difference in Water Level (Feet)")
    title = "Water Level (Observed - Predicted) since {} for {}".format(
        parse_year(location.start_date), location.get_station_name()
        )
    plt.title(title)
    plt.tight_layout()
    
    save_or_display_graph(plt, figname)

def graph_avg_water_by_month(df, location, figname=None):
    plt.clf()
    df = df.reset_index()
    # print("graph_avg_water_by_month()\n{}".format(df))
    ax = sns.lineplot(df, x=df['Month'].astype(str), y='Water Level', color='b',
                      label='Observed Water Level', legend='brief')
    sns.lineplot(df, x=df['Month'].astype(str), y='Prediction', ax=ax, color='orange',
                      label='Predicted Water Level', legend='brief')
    ax.xaxis.set_major_locator(ticker.LinearLocator(round(df.shape[0]/24)))
    ax.xaxis.set_label_text('Month')
    ax.yaxis.set_label_text('Water Level (Feet)')
    title = 'Average Monthly Water Levels Since {} for {}'.format(
        parse_year(location.start_date), location.get_station_name()
        )
    plt.title(title)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    save_or_display_graph(plt, figname)

def graph_month_avg_temps(temps, location, figname=None):
    plt.clf()

    ax = sns.lineplot(temps, x='Year-Month', y='Air Temp', color='g',
                legend='brief', label='Air Temp')
    sns.lineplot(temps, x='Year-Month', y='Water Temp', ax=ax, color='b',
                legend='brief', label='Water Temp')
    ax.xaxis.set_major_locator(ticker.LinearLocator(10))
    ax.xaxis.set_label_text('Month')
    ax.yaxis.set_label_text('Temperature (\N{DEGREE SIGN}F)')
    title = "Average Monthly Temperatures Since {} for {}".format(
        parse_year(location.start_date), location.get_station_name()
        )
    plt.title(title)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout(pad=2) # for displayed graph to not cut off x-axis labels
    
    save_or_display_graph(plt, figname)