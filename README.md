# MagicAssesment for Sandeep Suresh

First and foremost, thank you so much for the opporunity to redo this challenge without using pandas. I hope this new iteration can better highlight my 
capabilities in python.

# Important Notes about Running
  I put all of the libraries I needed in a requirements.txt, didn't want to upload my entire virtual environment. All the code is run in
  readWeather.py using python3.7. So should be able to just run it with the given requirements with: python3 readWeather.py, after repo 
  is cloned. Tests are commented out.

## Reading in the Data
  Instead of relying heavily on the pandas framework, I read the data in using the csv reader. For readability purposes, I also created a
  namedTuple called Reading, and stored all the rows from the csv as such.

## Part 1 getMinimumTemperatureStation
  Can't really beat O(n) in terms of finding a min value in unsorted data, so algorithm was pretty straight foward. I go through the entire
  list and compare temperatures, saving the row of the min temperature after a new miniumum is found. 

## Part 2 getStationWithMostFluctuation
  There were a couple assumptions I didn't want to make about the data that was true about the input data, but might not be true about other 
  weather data in this format that guided how I created the algorithm for this part. With the current data, all the weather readings come in 
  grouped by station, as in if you are reading top down, you will get all the readings for a particularlar station before reading another 
  station's readings. As a result, you could compute fluctuation for each station by reading the entire csv _only_ once because you would know
  you'd never get anymore readings from a station after you find a new station. I didn't make this assumption, so I grouped the temp readings by
  station in a map and then for each station computated fluctuation. I did, however, make the assumption that the data would be time sorted because
  an actual weather station would probably output readings sequentially. If this were not true, a sort by time would have to be done on all the temp
  readings before calculating fluctuation.
  
## Part 3 getStationWithMostFluctuationTimeBound
  Part 3 used the helper functions created by part 2. In the group_by_station function, there are default parameters that allow for filtering by
  time. Once these bounds are checked in grouping the temperature readings, the problem because a part 2 problem and is passed to 
  find_max_fluctuation_station.
  
## Testing
  This is the area that if I had more time I would rigorously test more. Right now, my code makes a lot of assumptions that the data that I read 
  will be correct and there are no 'gotchas'. For example, what if a row had a temperature reading that was actually a string? Or what if there
  was any missing data in any columns.
  
## Final Thoughts 
  Thank you for the opp
