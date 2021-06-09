import pandas as pd
import numpy as np

def readDataset(filename: str) -> pd.DataFrame :
    df = pd.read_csv(filename) 
    # Note found there was no missing values so no cleaning required
    # no way to drop bad values while reading, so performance slow down
    # if needed though just add: df.dropna(inplace=true)
    return df
    

def getMinimumTemperatureStation(df: pd.DataFrame) -> object:
    # Grabs index of row with lowest value in each column
    indices = df.idxmin()

    # Get row by index^ with lowest temp from temp column
    row = df.iloc[indices['temperature_c']]

    # Format return value
    stationInfo = {
        'station_id' : int(row['station_id']),
        'temperature_c': row['temperature_c']
    }
    return stationInfo

def getStationWithMostFluctuation(df: pd.DataFrame) -> int:
    # Group by station id, then calculate fluctuation for each station
    # Overriting temperature column with difference in series, applying absolute value to all differences, then summing them up
    groupedDf = df.groupby("station_id")["temperature_c"].apply(np.diff).apply(np.abs).apply(np.sum)
    station_id = groupedDf.idxmax()
    
    # fluctuation = groupedDf[station_id]
    # print("Fluctuation is: {0}".format(fluctuation))
    return station_id

def getStationWithMostFluctuationTimeBound(df: pd.DataFrame, startTime: float, endTime: float) -> int: 
    # Error check time bounds
    if(startTime > endTime) :
        print("Invalid time bounds")
        return -1
    
    # First filter any station that is not within time frame
    filteredDf = df.loc[(df['date'] >= startTime) & (df['date'] <= endTime)]

    # Now we've broken it down to part 2
    station_id = getStationWithMostFluctuation(filteredDf)
    return station_id

def output(lowestTempStation: object, stationWithMostFluctuation: int, stationWithMostFluctuationTimeBound: int,
           startTime: float, endTime: float) -> None:
    lowestStationString = "The station with the lowest temperature recording was {0}, with a reading of {1} Celcius\n".format(lowestTempStation["station_id"],lowestTempStation["temperature_c"])
    stationWithMostFluctuationString = "Station {0} had the most temperature fluctuation given all the readings\n".format(stationWithMostFluctuation)
    stationTimeBoundFluctuationString = "Station {0} with the most temperature fluctuation between {1} and {2}".format(stationWithMostFluctuationTimeBound, startTime, endTime)

    # Print
    print(lowestStationString + stationWithMostFluctuationString + stationTimeBoundFluctuationString) 

def tests() :  
    filename = 'data/test2.csv'
    testDf = readDataset(filename)

    # Note test data is just some readings from stations 68 and 81
    # with some modificiations to individual values

    # Part 1
    lowestTempStationObj = getMinimumTemperatureStation(testDf)
    assert(lowestTempStationObj['temperature_c'] == 5.4)
    assert(lowestTempStationObj['station_id'] == 100)

    # Part 2
    mostFluctuationStation = getStationWithMostFluctuation(testDf)
    assert(mostFluctuationStation == 100)

    # Part 3
    # Has only select data with some dates out of bound
    # If data out of bound is read, 81 should have highest fluctuation
    timeBoundStation = getStationWithMostFluctuationTimeBound(testDf, 2000.001, 2001.000)
    assert(timeBoundStation == 68)


def main() :
   
    # tests()
    
    # Read raw data
    filename = 'data/data.csv'
    rawDf = readDataset(filename)

    # Part 1
    lowestTempStation = getMinimumTemperatureStation(rawDf)

    # # Part 2
    mostFluctuationStation = getStationWithMostFluctuation(rawDf)

    # Part 3
    # Not sure what time range should be added here, used one in doc
    timeBoundStation = getStationWithMostFluctuationTimeBound(rawDf, 2000.001, 2000.456)

    # Output
    output(lowestTempStation, mostFluctuationStation, timeBoundStation, 2000.001, 2000.456)


if __name__ == "__main__":
    main()



