# MagicAssesment for Sandeep Suresh

First and foremost, thank you so much for the opporunity to take this challenge. I hadn't used pandas and numpy since my time at Nordstrom, 
so it was nice to revisist some of the tech. 

# Important Notes about Running
  I put all of the libraries I needed in a requirements.txt, didn't want to upload my entire virtual environment. All the code is run in
  readWeather.py using python3.7 So should be able to just run it with the given requirements with: python3 readWeather.py. Tests are commened out.

## General Thoughts
  I knew my biggest bottleneckwas reading in the data from the zip file. As a result, I only read it once and stored it in the dataframe. 
  I wanted to modularize the code as much as possible for readabiltly purposes and to limit rewriting of code. As seen in part 3, part 3 
  can be broken down to a part 2 problem after you filter out readings that are not in the time bounds. Similarly, if part 1 was also asked
  to have a time bound constraint, I could filter out the dates similarly and pass that dataframe into getMinimumTemperatureStation()

## Part 1 getMinimumTemperatureStation
  This was pretty straightforward after I have read in the data to my dataframe. Pandas supports finding the index of the min value for a 
  column, so I used that then created an object that stores the station id and the corresponding lowest temperature.

## Part 2 getStationWithMostFluctuation
  This was a little trickier, as originally I thought that "most fluctuation" would also mean "highest standard deviation." In an earlier
  version of my code (not shown in commits), the implementation of this part was easier as std() is a built in function for panda series, where
  as total fluctuation is not. After some testing, I found this initial assumption was not true, and thus resorted to calculating fluctuation 
  itself, which is a little more inefficient than std. If I had more time, I would research if there is a more efficient way to calculate total 
  fluctuation because right now I calculate the differences between temperatures, than convert them all to absolute values, then sum it up. More
  research would allow me to understand if there was a way I could do this in less passes.
  
## Part 3 getStationWithMostFluctuationTimeBound
  This was quite trivial after solving part 2 because part 3 can be broken down into a part 2 problem. After I filtered out the data in the dataframe
  that was not in the bounds of the time, I could just then call getStationWithMostFluctuation with my edited dataframe, as all the readings in this 
  dataframe are within the correct time bounds.
  
## Testing
  This is the area that if I had more time I would rigorously test more. Right now, my code makes a lot of assumptions that the data that I read 
  will be correct and there are no 'gotchas'. For example, what if a row had a temperature reading that was actually a string? Or what if there
  was any missing data in any column (note solution to this is trivial and is talked about in my code, just left out for performance reasons)
  
## Final Thoughts 
  To be honest, pandas this kind of data engineering work is not my forte. My experience with working with these technologies was only during my 
  time as a Machine Learning Engineer at Nordstrom. My python experiences are a lot more oriented around creating clients to test services, and 
  making and handling api calls. Regardless, I hope my work here was enough to get me to the next round, and if not thank you for reading this far :)
