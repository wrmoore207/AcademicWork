"""
Generic helper functions

DS5110 Fall 2023 Project Team 8 SDG

2023-11-07

:Authors:
Lukas Hernandez <hernandez.lu@northeastern.edu>
Johnathan Green <green.john@northeastern.edu>
Ryan Moore <moore.will@northeastern.edu>
"""

from datetime import datetime

def save_csv(df, filename, save_index=False):
    """
    Saves the supplied Pandas DataFrame to disk as specified
    """

    df.to_csv(filename, index=save_index)

def parse_year(date_str):
    """
    Parse year from string in format "20230501"
    """
    
    year = datetime.strptime(date_str, "%Y%m%d").year

    return year

def calc_last_day_of_month(start_month, year, day_num=1):
    """
    Calculates the last day of the month
    """

    # calculate day_offset based on month & year
    if (start_month in "01,03,05,07,08,10,12"):
      # jan, mar, may, july, aug, oct, dec have 31 days
      day_offset = 31 - day_num
    elif (start_month in "04,06,09,11"):
      # apr, jun, sept, nov have 30 days
      day_offset = 30 - day_num
    elif (year % 400 == 0 | (year % 4 == 0 & year % 100 != 0)):
      # leap years: year divisible by 4 or 400, but not 100
      # leap year, feb has 29 days
      day_offset = 29 - day_num
    else:
      # non-leap year, feb has 28 days
      day_offset = 28 - day_num

    # print(f"yyyymm day_offset: {start_year + start_month}, {day_offset} days")

    return day_offset

# convenience function to save or display a graph
def save_or_display_graph(plt, figname=None):
    # save or display the graph
    if figname is not None:
        plt.savefig(str(figname), bbox_inches='tight')
    else:
        plt.show()
