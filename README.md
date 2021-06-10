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

## Part 1 get_minimum_temperature_station
  Can't really beat O(n) in terms of finding a min value in unsorted data, so algorithm was pretty straight foward. I go through the entire
  list and compare temperatures, saving the row of the min temperature after a new miniumum is found. 

## Part 2 get_station_with_most_fluctuation
  I wanted my code to be extendable and robust, so that even if the data didn't present itself like it did now weatherprocessor.py would still work.
  In the data given, all the weather stations were already grouped together and sorted by time and as a result fluctuation can be done in pass without
  much extra things to store. However, I wanted my code to work even if station readings were interweaved but still timesorted (as I felt a normal 
  weather sensor would probably output data sequentially). Thus, I added a map that stores the previous val for each station to solve this. However,  
  I recognize my solution can't be modularized much. Another version of my code is more readable, as I extracted all the temp readings for each station
  then calculated fluctuation for each station then in a different function. This was more clean, but at the cost of performance as I pass through the data
  multiple times. 
  
## Part 3 get_station_with_most_fluctuation_time_bound
  Part 3 relied heavily on part two. The filtering can be done in the second method, so this method really just does some error checking on the bounds,
  then passes it over to part two. I still created a seperate function, so that a user could still easily call this endpoint without any confusion. 
  
## Testing
  This is the area that if I had more time I would rigorously test more. Right now, my code makes a lot of assumptions that the data that I read 
  will be correct and there are no 'gotchas'. For example, what if a row had a temperature reading that was actually a string? Or what if there
  was any missing data in any columns.
 
