# DS5110 Fall 2023 - U.N. Sustainability Development Goals
Contents
* [Project Team](#team)
* [Stakeholder](#stakeholder)
* [Story](#story)
* [Dependencies](#dependencies)
* [Proposal](#proposal)
* [Plan](#plan)
* [Exploratory Data Analysis](#eda)
* [Lessons Learned](#learnings)
* [Visualizations](#visuals)
* [Data](#data)

<a name="team"></a>
## Project Team - Team 8
* Johnathan Green (team lead) <green.john@northeastern.edu>
* Lukas Hernandez <hernandez.lu@northeastern.edu>
* Ryan Moore <moore.will@northeastern.edu>

<a name="stakeholder"></a>
## Project Stakeholder
Dr Susana Hancock, Science Manager, [Arctic Base Camp](https://arcticbasecamp.org/)
  * [Arctic Risk Platform](http://arcticrisk.org/)

<a name="story"></a>
## Story
  * Greenland is currently the largest contributor to ocean sea level rise around the world, 
  and a minimum of 10 inches is locked in because of the destabilization of its ice sheet. 
  The 10in of sea level rise, however, will not be felt universally around the world; 
  some places will experience more rise than others.
  This creates a huge climate justice issue, as many of those most affected by sea level 
  rise have done the least to contribute to the problem. 
  We are currently working on policies that bring international attention to the impact 
  of sea level rise on climate vulnerable regions around the world to global leaders 
  (including ambassadors, heads of state, business CEOs) at events such as the UN COPs, 
  the World Economic Forum, Reuters Impact series, New York Climate Week, the UN General Assembly, etc. 
  In this process, we work with the Climate Vulnerable Forum (58 most climate vulnerable countries) and 
  through the UN Sustainable Development Goals (SDGs). 
  * The problem is also hyperlocal.  Just 1.6ft rise in ocean levels could submerge 67% of coastal sand 
  dunes along the coast of Maine. Parts of Commercial Street---built on top of old piers in the 1850s with 
  fill pushed into Casco Bay—-are already contending with tidal flooding, which is harming local businesses, 
  residences and infrastructure. The "Maine Won’t Wait" climate action plan is recommending the state accommodate 
  for 1.5 feet of relative sea level rise by 2050 and 3.9 feet of relative rise by 2100. However, without drastic 
  emissions cuts, this may not be sufficient, and some researchers are suggesting we may want to prepare 
  for 8’ of sea level rise by the end of the century. There is still time to make amendments to the policy, 
  but it will become increasingly challenging as more coastal (and not-so-coastal) towns solidify their 
  climate plans.
  * For this project, we want to understand and visualize the relationship between existing measurements 
  of sea levels (rate, extent of change) and the future predictions under various scenarios, 
  especially for the state of Maine. 
  Can we detect the effects of climate change in the measurements? 
  What is flooded at low and high tides? 
  How do the current tides and sea level measurements around the state relate to the 
  worst-case scenario (not just average but MAX)? Who/what is impacted and at what timeframes (2030, 2050, 2100, etc.)?
  Sea level rise in the Gulf of Maine is directly related to several of the UN Sustainable Development Goals
  (SDGs): Including (but not limited to) #6 clean water and sanitation (salt water intrusion); #8 economic
  growth (affects the working waterfront); #9 industry and infrastructure (damage to infrastructure
  already happening, new designs); #13 climate action (polar melt+thermal expansion driving the rise);
  #14 life below water (affects the health of seas and marine resources.

<a name="dependencies"></a>
## Dependencies
- numpy=1.26.0
- pandas=2.1.1
- matplotlib=3.8.0
- seaborn=0.13.0
- scikit-learn=1.3.2
- requests=2.31.0

### Miniconda Environment
If desired, a miniconda environment can be setup and used to install the dependencies for running the project code.

```bash
conda env create -f environment.yml && conda activate ds5110_fall2023_team_8
```

<a name="proposal"></a>
## Proposal

[Proposal](proposal.md)

<a name="plan"></a>
## Plan

[Plan](plan.md)

<a name="eda"></a>
## Exploratory Data Analysis

[EDA](eda.md)

<a name="learnings"></a>
## Lessons Learned

1. Retreiving data proved to be more effort than initially thought since we wanted to get all available data and certain data from the NOAA Tides & Currents data had to be pulled one month at a time. This applies to the 6-minute interval water level, water temperature, and air temperature data.
1. Due to the extent of the data we wanted to work with, it proved important to save copies of the "cleaned" data. The download of raw data took long and doing that repeatedly was hindering progress.
1. Initially we were using a Google Collab notebook to develop code. Once the code started to become substantial, working in Collab became difficult quickly.
1. Refactoring the data download code to support other NOAA Tides stations beyond Portland was a challenge due to the starting assumption that our project would only include Portland. The code was not designed in a flexible manner to make that support easy. We ultimately introduced a class to pass through input parameters for pulling the different types of data for the range of dates and stations we wanted.

<a name="visuals"></a>
## Visualizations

#### Water Levels and Air & Water Temps Demo

There is a demo script that can be run to see some things that we have been able to do with the data so far.
Currently:
* Shows EDA image for all Maine stations
* Shows an average of predicted water level - measured water level over a week for all Maine stations
* Shows an average of predicted water level - measured water level for all Maine stations
* Shows monthly average of measured water level compared with predicted water level since for all Maine stations
* Shows monthly average of air and water temperatures since for all Maine stations

```bash
make tides_demo
```

#### Storm Winds Demo

The storm winds demoscript displays graphs of
* Number of storms per year
* Storms per year vs predicted * storms per year
* Average monthly storms per year

```
make storm_visuals
```

<a name="data"></a>
## Data

Data details for this project and how to load the data are described in the following sections.

#### NOAA Tides and Currents Data Products (water levels, air temperatures, water temperatures)

|Type of Data|NOAA Tides product name|
|------------|-----------------------|
|6-minute Interval Air Temperatures		|`air_temperature`	|
|6-minute Interval Water Temperatures	|`water_temperature`|
|Hourly Interval Water Levels			|`hourly_height`	|
|6-minute Interval Verified Water Levels|`water_level`		|

##### Tides Data Availability Start Years by Product and Station

|Station|Water Levels (6-min interval)|Water Levels (hourly interval)|Water Temps|Air Temps|
|-------|--------------------------------|------------------------------|-----------|---------|
|[8410140 Eastport](https://tidesandcurrents.noaa.gov/inventory.html?id=8410140)			|1996|1929|1991|1995|
|[8411060 Cutler Farris Wharf](https://tidesandcurrents.noaa.gov/inventory.html?id=8411060)	|2010|2010|2010|2010|
|[8413320 Bar Harbor](https://tidesandcurrents.noaa.gov/inventory.html?id=8413320)			|1997|1947|2008|1999|
|[8418150 Portland](https://tidesandcurrents.noaa.gov/inventory.html?id=8418150)			|1996|1910|2009|1997|
|[8419870 Seavey Island](https://tidesandcurrents.noaa.gov/inventory.html?id=8419870)		|1998|1926|2021|2021|

<a name="downloadtidesdata"></a>
##### Download Tides Data

The NOAA Tides data can be downloaded for all Maine stations by following the instructions in [Tides Data Download](tides_data_download.md).
**NOTE: It is not required to do this before running the project. The project will leverage the checked-in "clean" data files.**

##### Load the Tides Data
This program loads NOAA Tides and Currents data as a Pandas DataFrame. It accepts a `Location` object and data `product` for which it will load the data. The `Location` object specifies a date range and NOAA Tides and Currents station to load data for.

For more information: [load_tides.md](load_tides.md)

#### NCEI Storm Winds Dataset Summary and Download Instructions

To explore the occurrence of storms and storm winds in particular, we used [NCEI Storm Events Database](https://www.ncdc.noaa.gov/stormevents/choosedates.jsp?statefips=23%2CMAINE). The records begin in the late 1950s and track reports of weather events including thunderstorm, hurricanes, and other storm event types.

Downloading the data from the NCEI is not necessary to run the programs in this notebook. There is a cleaned dataset saved in the data folder

To download the data from NCEI run:

```
make get_storms
```

### Data Sources
* [NOAA tides and water-level measurements](https://tidesandcurrents.noaa.gov/waterlevels.html?id=8418150)
  * [CO-OPS API For Data Retrieval](https://api.tidesandcurrents.noaa.gov/api/prod/)
* [NCEI Storm Events Database](https://www.ncdc.noaa.gov/stormevents/choosedates.jsp?statefips=23%2CMAINE)
  * [Bulk Data Download](https://www.ncdc.noaa.gov/stormevents/ftp.jsp)
