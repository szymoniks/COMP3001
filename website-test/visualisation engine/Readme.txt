Status of Work on Python Data Analyser

1. Uses python to read a csv file from the bike usage archive of TFL (bigsample.csv is an example)
2. When supplied a csv file in the format specified by TFL, it is so far able to:
	a. Calculate Earliest and latest dates of that data chunk, and all dates in between
	b. Calculate Bike gain (number of bikes returned to dock) on the earliest date of that data chunk for all docks. Docks with no movement will not be documented
	c. Do similare calculations for Bike losses
	d. Return a dictionary of net gains/losses of all stations for the earliest date specified
3. Work still in Progress: 
	a. Calculate for all dates
	b. Format and produce xml file
	c. Automate and work on succession of csv files
