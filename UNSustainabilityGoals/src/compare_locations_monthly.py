import location_class
from data_editing import average_by_month
from data_editing import find_waterlvl_diff_avg_month
from helpers import save_or_display_graph
from datetime import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

portland = location_class.setup_station_by_data_product('portland', 'water_level')
eastport = location_class.setup_station_by_data_product('Eastport', 'water_level')
cutler = location_class.setup_station_by_data_product('Cutler Farris Wharf', 'water_level')
seavey = location_class.setup_station_by_data_product('Seavey Island', 'water_level')
bar_harbor = location_class.setup_station_by_data_product('Bar Harbor', 'water_level')

port_df = average_by_month(portland)
east_df = average_by_month(eastport)
cutler_df = average_by_month(cutler)
seavey_df = average_by_month(seavey)
bar_harbor_df = average_by_month(bar_harbor)

#Fills in NaN for missing data
seavey_df = seavey_df.set_index('Month')
new_dates = pd.date_range(start=seavey_df.index[0], end=seavey_df.index[-1], freq='M')
seavey_df = seavey_df.reindex(new_dates.strftime("%Y-%m"))

bar_harbor_df = bar_harbor_df.set_index('Month')
new_dates = pd.date_range(start=bar_harbor_df.index[0], end=bar_harbor_df.index[-1], freq='M')
bar_harbor_df = bar_harbor_df.reindex(new_dates.strftime("%Y-%m"))

fig, ax = plt.subplots(1,1)
ax.plot(port_df["Month"], port_df["Water Level"], label="Portland")
ax.plot(east_df["Month"], east_df["Water Level"], label="Eastport")
ax.plot(seavey_df.index, seavey_df["Water Level"], label="Seavey Island")
ax.plot(cutler_df["Month"], cutler_df["Water Level"], label="Cutler Farris Wharf")
ax.plot(bar_harbor_df.index, bar_harbor_df["Water Level"], label="Bar Harbor")
ax.xaxis.set_major_locator(ticker.LinearLocator(round(port_df.shape[0]/24)))
plt.xticks(rotation=45)
plt.xlabel("Date")
plt.ylabel("Water Level(Feet)")
plt.title("Average Monthly Water Level")
plt.legend()
plt.tight_layout()
figname = "figs/avg_monthly_complete.png"
save_or_display_graph(plt, figname)
plt.show()

