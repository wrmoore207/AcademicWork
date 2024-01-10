import location_class
from data_editing import average_by_month
import seaborn as sns
import matplotlib.pyplot as plt
from helpers import save_or_display_graph



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

locations = [port_df, east_df, cutler_df, seavey_df, bar_harbor_df]
location_name = ["Portland", "Eastport", "Cutler Farris Wharf", "Seavey Island", "Bar Harbor"]
for n in range(len(locations)):
    locations[n]['Index'] = range(len(locations[n]))
    sns.regplot(data=locations[n], x='Index', y='Water Level', scatter_kws={'color':'black'}, line_kws={'color':'red'})
    plt.xlabel("Time")
    plt.ylabel("Water Level")
    plt.title(f"{location_name[n]} Monthly Average Sea Level")
    plt.tight_layout()
    figname = f"figs/avg_monthly_{location_name[n]}_regplot.png"
    save_or_display_graph(plt, figname)
    plt.show()
