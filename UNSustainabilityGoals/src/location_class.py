class Location:
    def __init__(self, start_date, end_date, station_id):
        self.start_date = start_date
        self.end_date = end_date
        self.station_id = station_id

    def __str__(self):
        output = "start_date={}, end_date={}, station_id={}".format(
            self.start_date, self.end_date, self.station_id)
        return output
    
    def get_station_name(self):
        stations = {
            "8418150" : "Portland",
            "8410140" : "Eastport",
            "8411060" : "Cutler Farris Wharf",
            "8419870" : "Seavey Island",
            "8413320" : "Bar Harbor"
        }

        return stations[self.station_id]

    def get_station_data_start_year(self, product):
        portland_first_years = {
            "water_level" : "1996",
            "water_temperature" : "1997",
            "hourly_height" : "1910",
            "air_temperature" : "2009"
        }

        eastport_first_years = {
            "water_level" : "1996",
            "water_temperature" : "1995",
            "hourly_height" : "1929",
            "air_temperature" : "1991"
        }

        cutler_farris_wharf_first_years = {
            "water_level" : "2010",
            "water_temperature" : "2010",
            "hourly_height" : "2010",
            "air_temperature" : "2010"
        }

        seavey_island_first_years = {
            "water_level" : "1998",
            "water_temperature" : "2021",
            "hourly_height" : "1926",
            "air_temperature" : "2021"
        }

        bar_harbor_first_years = {
            "water_level" : "1997",
            "water_temperature" : "1999",
            "hourly_height" : "1947",
            "air_temperature" : "2008"
        }

        first_year_available = {
            "8418150" : portland_first_years,
            "8410140" : eastport_first_years,
            "8411060" : cutler_farris_wharf_first_years,
            "8419870" : seavey_island_first_years,
            "8413320" : bar_harbor_first_years
        }
        
        return first_year_available[self.station_id][product]

def get_station_id(station_name):
    stations = {
        "portland" : "8418150",
        "eastport" : "8410140",
        "cutler farris wharf (cfw)" : "8411060",
        "seavey island (si)" : "8419870",
        "bar harbor (bh)" : "8413320"
    }

    # make station match more flexible
    for key in stations.keys():
        if station_name.lower() in key:
            return stations[key]
    
    # default station is Portland
    return stations['portland']

def setup_station_one_week(station_name):
    station_id = get_station_id(station_name)

    year = "2023"
    month = "05"
    day = "01"
    start_date = year + month + day
    end_day = str(int(day) + 6).rjust(2, '0')
    end_date = year + month + end_day

    return Location(start_date, end_date, station_id)

def setup_station_by_start_year(station_name, year):
    station_id = get_station_id(station_name)

    start_date= year + "0101"
    end_date="20230930"

    location = Location(start_date, end_date, station_id)

    return location

def setup_station_by_data_product(station_name, product):
    station_id = get_station_id(station_name)
    location = Location(None, None, station_id)

    start_date = location.get_station_data_start_year(product) + "0101"
    end_date="20230930"

    location.start_date = start_date
    location.end_date = end_date
    
    location = Location(start_date, end_date, station_id)

    return location
