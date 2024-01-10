"""
Saves a figure of 1 week's NOAA Tides and Water Levels data for Portland, ME

DS5110 Fall 2023 Project Team 8 SDG

EDA Milestone 2023-10-14

:Authors:
Lukas Hernandez <hernandez.lu@northeastern.edu>
Johnathan Green <green.john@northeastern.edu>
Ryan Moore <moore.will@northeastern.edu>
"""

from tides_visualizations import make_eda_by_station


station = 'portland'
make_eda_by_station(station)
