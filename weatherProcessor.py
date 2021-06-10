from csv import reader
from typing import List, Dict
import zipfile
from collections import namedtuple

from pandas.core.tools import numeric
# Named tuple for readability and rows
Reading = namedtuple('Reading', 'id date temp')


def read_zip_dataset() -> List[Reading]:
    """
    Reads zip file and extracts to data folder

    Returns:
        List: All the readings from data/data.csv
    """
    with zipfile.ZipFile('data/data.csv.zip') as zip:
        print("Unzipping data.csv.zip")
        zip.extractall('data/')
        return read_dataset('data/data.csv')


def read_dataset(filename: str) -> List[Reading]:
    """
        Reads a csv file into namedTuples called Reading
    Args:
        filename (str): path to csv file

    Returns:
        List[Reading]: All the readings from the csv file
    """
    print("Starting to read: " + filename)
    with open(filename) as csvfile:
        csv_reader = reader(csvfile)
        next(csv_reader)  # Skip header
        # Throw all readings into a list of named tuples, casted to types
        rows = [Reading(int(row[0]), float(row[1]), float(row[2])) for row in list(csv_reader)]
        print("Finished reading in data from: " + filename)
        return rows


def get_minimum_temperature_station(table: List[Reading]) -> Dict:
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
        if row.temp < min_temp:
            min_row = row
            min_temp = row.temp
    station_info = {
        'station_id' : min_row.id,
        'date': min_row.date
    }

    return station_info

def get_station_with_most_fluctuation(table: List[Reading], start_date=None, end_date=None) -> int:
    """
    Main function that kicks off the different processes needed to find the 
    station with the most fluctuation

    Args:
        table (list): table for all csv data

    Returns:
        int: retuns station id with the most fluctuation
    """

    # Will still work if readings are not grouped by station, so long as time sorted

    timeBound = False
    if start_date is not None and end_date is not None:
        timeBound = True

    prev_val_map = {}
    fluctuation_map = {}
    max_fluctuation = 0
    max_station = 0
    for row in table :
        if row.id in fluctuation_map:
            # Check if within time bounds if necessary 
            if timeBound and (row.date < start_date or row.date > end_date):
                continue
            # Update fluctuation for station and check if > max
            fluctuation_map[row.id] += abs(row.temp - prev_val_map[row.id])
            if fluctuation_map[row.id] > max_fluctuation:
                max_station = row.id
                max_fluctuation = fluctuation_map[row.id]
        else:
            fluctuation_map[row.id] = 0

        # Always update prev value for station, assuming time sorted
        prev_val_map[row.id] = row.temp

    return max_station


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

    return get_station_with_most_fluctuation(table, start_date, end_date)


def tests() -> None:  
    filename = 'data/test.csv'
    test_table = read_dataset(filename)

    # Note test data is just some readings from stations 68 and 81
    # with some modificiations to individual values

    # Part 1
    lowest_temp_station = get_minimum_temperature_station(test_table)
    assert(round(lowest_temp_station['date'], 3) == 2000.542), "Incorrect date for the station with the lowest temp!"
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

    tests()

    # Read raw data
    table = read_zip_dataset()
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