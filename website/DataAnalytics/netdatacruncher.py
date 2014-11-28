import csv
import os
from string import *
from datetime import datetime as dt
from datetime import date
from datetime import time
from datetime import timedelta
import xml.etree.ElementTree as et
from xml.dom import minidom
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

path = 'C:/Python27/Scripts/'
#convert date in string format to datetime format
#arg0: date time string
def convertDate(string):
	try:
		condate = dt.strptime(string, "%d/%m/%Y %H:%M")
	except ValueError:
		condate = dt.strptime(string, "%d/%m/%Y %H:%M:%S")
	return condate

def killrogues(reader):
	print convertDate(reader.next()['Start Date']).date()
	for row in reader:
		if convertDate(row['Start Date']).date() < date(2012,1,1) or convertDate(row['End Date']).date() < date(2012,1,1):
			print "killing rogues", str(row)
			del row

#calculate earliest date in data segment return in date format
#arg0: reader for csv file
def getEarliestDate(reader):
	rd = reader
	earliest = convertDate(rd.next()['Start Date'])
	for row in rd:
		if convertDate(row['Start Date']) < earliest and convertDate(row['Start Date']).date() > date(2012,1,1):

			earliest = convertDate(row['Start Date'])


	return earliest.date()

#calculate latest date in data segment return in date format
#arg0: reader for csv file
def getLatestDate(reader):
	rd = reader
	latest = convertDate(rd.next()['Start Date'])
	for row in rd:
		if convertDate(row['Start Date']) > latest:
			latest = convertDate(row['Start Date'])

	return latest.date()

#input fresh iterator and date of day, return bike loss for that day for each station 
#in a dict
#arg0: reader for csv file, 
#arg1: date object
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

#similar to getBikeLoss
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
#arg0: bikeloss dict
#arg1: bikegain dict
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
#arg0: iterator of readers for csv file
#arg1: date object
def getNet(mainreader, day):
	bikegain = getBikeGain(iter(mainreader), day)
	bikeloss = getBikeLoss(iter(mainreader), day)
	net = getNetMovement(bikeloss, bikegain)
	return net

#helper function to indent xml file
#arg0: elementtree element
def prettify(elem):
	rough_string = et.tostring(elem, 'utf-8')
	reparsed = minidom.parseString(rough_string)
	return reparsed.toprettyxml()

#Major function to produce the xml file from read csv file
#arg0: earliest date object
#arg1: latest date object
#arg2: list of iterator of csv reader
#arg3: namelist dict
def writeXml(earliest, latest, mainreader, namelist, filename):
	root = et.Element("dailydata")
	root.set('version', '1.0')
	comment = et.Comment("Generated for COMP3001 by netdatacruncher.py -zhilim")
	root.append(comment)
	print "writing to xml.."
	next = earliest
	while next <= latest:
		print "writing data for ", str(next)
		date = et.SubElement(root, "date")
		date.set('name', str(next))
		gain = getBikeGain(iter(mainreader), next)
		loss = getBikeLoss(iter(mainreader), next)
		netdict = getNetMovement(loss, gain)
		netkeys = iter(netdict)
		hasnext = True
		while hasnext:

			try:
				nextkey = netkeys.next()
				#print "writing next station's data"
				stationId = et.SubElement(date, "stationId")
				stationId.set('name', nextkey)

				stationNm = et.SubElement(stationId, "stationNm")
				stationNm.text = namelist[nextkey]

				net = et.SubElement(stationId, "net")
				net.text = str(netdict[nextkey])

				bikeloss = et.SubElement(stationId, "bikeloss")
				bikegain = et.SubElement(stationId, "bikegain")

				if nextkey in loss:
					bikeloss.text = str(loss[nextkey])
				else:
					bikeloss.text = "0"

				if nextkey in gain and nextkey in loss:
					bikegain.text = str(netdict[nextkey] + loss[nextkey])
				if nextkey in gain and nextkey not in loss:
					bikegain.text = str(netdict[nextkey])
				elif nextkey not in gain:
					bikegain.text = "0"

			except StopIteration:
				hasnext = False
		next = next + timedelta(days=1)	
	print "end of csv, prettifying.."
	#print et.tostring(root)
	try:			
		tree = prettify(root)
		with open(filename, "w") as f:
			f.write(tree)


	except UnicodeDecodeError:
		with open("C:/Python27/Scripts/log.txt", "a") as log:
			log.write("Unicode Decode Error with file: ".join(filename))
		print "error occurred."
		
	print "writing to:", filename
	
	

#function to update relation between station ID and station Name
#meant to be a sort of cache memory
#arg0: iterator of csv reader
#arg1: namelist dict (intialize before hand)
def updateNameList(reader, namelist):
	hasnext = True
	while hasnext:
		try:
			next = reader.next()
			if next['StartStation Id'] not in namelist:
				if next['StartStation Id'] == "729":
					namelist[next['StartStation Id']] = "St Peters Terrace, Fulham"
				else:
					namelist[next['StartStation Id']] = next['StartStation Name']

			if next['EndStation Id'] not in namelist:
				if next['EndStation Id'] == "729":
					namelist[next['EndStation Id']] = "St Peters Terrace, Fulham"
				else:
					namelist[next['EndStation Id']] = next['EndStation Name']

		except StopIteration:
			hasnext = False
	return namelist


#main function
def dataCrunch(csvfilename):
	print "crunching for", csvfilename
	with open(csvfilename,
		'rb') as csvfile:
		reader = list(csv.DictReader(csvfile))

		#killrogues(iter(reader))
		print "Calculating Earliest and Latest dates of data segment..."
		earliest = getEarliestDate(iter(reader))
		latest = getLatestDate(iter(reader))
		print "Earliest:", str(earliest)
		next = earliest + timedelta(days=1)
		while next < latest:
			print "Next:", str(next)
			next = next + timedelta(days=1)
		print "Latest:", str(latest)

		namelist = {"0": "None"}
		print "Updating namelist..."
		namelist = updateNameList(iter(reader), namelist)
		#print namelist
		#print namelist
		xmlfilename = csvfilename.replace(".csv", ".xml")

		writeXml(earliest, latest, reader, namelist, xmlfilename)


for filename in os.listdir(path):
	if not filename.endswith('.csv'):
		continue
	fullname = os.path.join(path, filename)
	print fullname
	dataCrunch(fullname)
