import pandas as pd
import numpy as np
import sys 
from csv import reader
from typing import List, Dict
import zipfile
from collections import namedtuple
# Named tuple for readability and rows
Reading = namedtuple('Reading', 'id date temp')

def readZipDataset() -> List: 
    """
    Reads zip file and extracts to data folder

    Returns:
        List: All the readings from data/data.csv
    """
    with zipfile.ZipFile('data/data.csv.zip') as zip:
        print("Unzipping data.csv.zip")
        zip.extractall('data/')
        return readDataset('data/data.csv')
    

def readDataset(filename: str) -> List[Reading]:     
    """
        Reads a csv file into namedTuples called Reading 
    Args:
        filename (str): path to csv file

    Returns:
        List[Reading]: All the readings from the csv file
    """
    with open(filename) as csvfile :
        csv_reader = reader(csvfile)
        next(csv_reader) # Skip header
        # Throw all readings into a list of named tuples, casted to correct types
        list_of_rows = [Reading(int(row[0]), float(row[1]), float(row[2])) for row in list(csv_reader)]
        print("Finished reading in data from: " + filename)
        return list_of_rows

def get_minimum_temperature_station(table: List[Reading]) -> Dict[str]:
    """
    Gets the station with the lowest temperature reading

    Args:
        table (List[Reading]): csv data

    Returns:
        Dict[str]: map that has station_id and date of lowest temp reading
    """
    # Go through entire temp column and return the min val O(n)
    min_temp = float("inf")
    min_row = []
    for row in table :
        if row.temp < min_temp :
            min_row = row
            min_temp = row.temp
    station_info = {
        'station_id' : min_row.id,
        'date': min_row.date
    }

    return station_info

def group_by_station(table: list, start_date=None, end_date=None) -> Dict[int]: 
    """ 
    Groups stations by its temp readings and has ability to filter 
    based on time bounds

    Args:
        table (list): csv data
        start_date ([type], optional): lower time bound. Defaults to None.
        end_date ([type], optional): upper time bound. Defaults to None.

    Returns:
        dict: mapping between station id and corresponding temp readings
    """
    
    # Time Bound handling
    time_bound = False
    if start_date is not None and end_date is not None :
        time_bound = True

    station_map = {}
    for row in table :
        if row.id in station_map :
            # Continue if we are filtering with time and out of bounds
            if time_bound and (row.date < start_date or row.date > end_date) :
                continue
            station_map[row.id].append(row.temp)
        else :
            station_map[row.id] = [row.temp]

    return station_map

def find_max_fluctuation_station(station_map: Dict[int]) -> int:
    """
    Finds station with the most fluctuation

    Args:
        station_map (dict): maps station id to all its temp readings

    Returns:
        int: station_id with most fluctuation
    """
    max_fluctuation = 0
    max_station = 0
    for station in station_map :
        curr_fluctuation = get_fluctuation_for_station(station_map[station])
        if curr_fluctuation >= max_fluctuation :
            max_fluctuation = curr_fluctuation
            max_station = station
    return max_station
        

def get_fluctuation_for_station(temp_readings: List[float]) -> int:
    """ 
    Gets fluctuation for a specific station's readings
    
    Args:
        temp_readings (List): temp readings for the station

    Returns:
        int: total fluctuation for the station
    """
    # Also works but less readable
    # return sum([abs(curr-prev) for prev, curr in zip(temp_readings, temp_readings[1:])])

    fluctuation = 0
    for prev, curr in zip(temp_readings, temp_readings[1:]):
        fluctuation += abs(curr-prev)
    return fluctuation

def get_station_with_most_fluctuation(table: List[Reading], timeBound=False, startDate=None, endDate=None) -> int:
    """
    Main function that kicks off the different processes needed to find the 
    station with the most fluctuation

    Args:
        table (list): table for all csv data
        timeBound (bool, optional): whether we are looking at time data. Defaults to False.
        startDate ([type], optional): time lower bound. Defaults to None.
        endDate ([type], optional): time upper bound. Defaults to None.

    Returns:
        int: [description]
    """
    station_map = group_by_station(table)
    return find_max_fluctuation_station(station_map)



def get_station_with_most_fluctuation_time_bound(table: List[Reading], start_date: float, end_date: float) -> int: 
    """ 
    Function that kicks off necessary processes to get station with most fluctuation with a 
    given time bound

    Args:
        table (list): csv data
        start_date (float): lower time bound
        end_date (float): upper time bound

    Returns:
        int: station with most fluctuation within time bound
    """
    # Error checking
    try :
        if start_date > end_date : return -1
        if start_date is None or end_date is None: return -1
    except TypeError: 
        print("Error: Start date and end dates have to be floats")
        return -1

    station_map = group_by_station(table, start_date, end_date)
    return find_max_fluctuation_station(station_map)

def tests() -> None:  
    filename = 'data/test.csv'
    test_table = readDataset(filename)

    # Note test data is just some readings from stations 68 and 81
    # with some modificiations to individual values

    # Part 1
    lowest_temp_station = get_minimum_temperature_station(test_table)
    assert(round(lowest_temp_station['date'],3) == 2000.542), "Incorrect date for the station with the lowest temp!"
    assert(lowest_temp_station['station_id'] == 68), "Incorrect station for lowest temp, should be"

    # Part 2
    # Changed one temperature value in 81 to 5000 to ensure it gets most fluctuation
    most_fluctuation_station = get_station_with_most_fluctuation(test_table)
    assert(most_fluctuation_station == 81)

    # Part 3
    # If data is read out of the time bound 81 should have most, if it functions correctly, 68
    time_bound_station = get_station_with_most_fluctuation_time_bound(test_table, 2000.001, 2001.000)
    assert(time_bound_station == 68)

    # Ensure that a type error is thrown if date sent in is not a float
    time_bound_station = get_station_with_most_fluctuation_time_bound(test_table, 2000.001, "hello")
    assert(time_bound_station == -1)

    print("All tests passed!")

def main() :

    # tests()

    # Read raw data
    table = readZipDataset()
    # Part 1
    lowest_temp_station = get_minimum_temperature_station(table)
    print("The station with the lowest temperature recording was {0} at {1}".format(lowest_temp_station["station_id"],round(lowest_temp_station["date"], 3)))

    # Part 2
    station_with_most_fluctuation = get_station_with_most_fluctuation(table)
    print("Station {0} had the most temperature fluctuation given all the readings".format(station_with_most_fluctuation))

    # Part 3
    # Not sure what time range should be added here, used one in doc
    time_bound_station = get_station_with_most_fluctuation_time_bound(table, 2000.001, 2000.456)
    print("Station {0} with the most temperature fluctuation between {1} and {2}".format(time_bound_station, 2000.001, 2000.456))


if __name__ == "__main__":
    main()