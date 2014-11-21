import csv
from string import *
from datetime import datetime as dt
from datetime import date
from datetime import time
from datetime import timedelta

#convert date in string format to datetime format
def convertDate(string):
	return dt.strptime(string, "%d/%m/%Y %H:%M")

#calculate earliest date in data segment return in date format
def getEarliestDate(reader):
	rd = reader
	earliest = convertDate(rd.next()['Start Date'])
	for row in rd:
		if convertDate(row['Start Date']) < earliest:
			earliest = convertDate(row['Start Date'])

	return earliest.date()

#calculate latest date in data segment return in date format
def getLatestDate(reader):
	rd = reader
	latest = convertDate(rd.next()['Start Date'])
	for row in rd:
		if convertDate(row['Start Date']) > latest:
			latest = convertDate(row['Start Date'])

	return latest.date()
#input fresh iterator and date of day, return bike loss for that day for each station 
#in a dict
def getBikeLoss(reader, day):
	bikeloss = {"0" : 0}
	hasnext = True
	while hasnext:
		try:
			row = reader.next()
			if convertDate(row['Start Date']).date() == day:
				if row.get('StartStation Id') not in bikeloss:
					bikeloss[row.get('StartStation Id')] = 1
				else:
					bikeloss[row.get('StartStation Id')] += 1
		except StopIteration:
			hasnext = False
	del bikeloss["0"]
	#print bikeloss
	return bikeloss

def getBikeGain(reader, day):
	bikegain = {"0" : 0}
	hasnext = True
	while hasnext:
		try:
			row = reader.next()
			if convertDate(row['End Date']).date() == day:
				if row.get('EndStation Id') not in bikegain:
					bikegain[row.get('EndStation Id')] = 1
				else:
					bikegain[row.get('EndStation Id')] += 1
		except StopIteration:
			hasnext = False
	del bikegain["0"]
	#print bikegain
	return bikegain

#returns a dict of the difference of bike loss and gains
def getNetMovement(bikeloss, bikegain):
	net = bikegain
	losskeys = iter(bikeloss)
	hasnext = True
	while hasnext:
		try:
			nextkey = losskeys.next()
			if nextkey in net:
				net[nextkey] -= bikeloss[nextkey]
			else:
				net[nextkey] = -bikeloss[nextkey]
		except StopIteration:
			hasnext = False		
	return net

#consolidator function
def getNet(mainreader, day):
	bikegain = getBikeGain(iter(mainreader), day)
	bikeloss = getBikeLoss(iter(mainreader), day)
	net = getNetMovement(bikeloss, bikegain)
	return net


#main function
with open('bigsample.csv',
	'rb') as csvfile:
	reader = list(csv.DictReader(csvfile))
	print "Calculating Earliest and Latest dates of data segment..."
	earliest = getEarliestDate(iter(reader))
	latest = getLatestDate(iter(reader))
	print "Earliest:", str(earliest)
	next = earliest + timedelta(days=1)

	while next < latest:
		print "Next:", str(next)
		next = next + timedelta(days=1)

	print "Latest:", str(latest)
	print getNet(reader, earliest)


