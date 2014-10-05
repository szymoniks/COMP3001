import httplib
httplib.HTTPConnection.debuglevel = 1
import urllib2
request = urllib2.Request('http://www.tfl.gov.uk/tfl/syndication/feeds/cycle-hire/livecyclehireupdates.xml')
opener = urllib2.build_opener()
feeddata = opener.open(request).read()

print str(len(feeddata))
