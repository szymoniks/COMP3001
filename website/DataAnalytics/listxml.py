import os
import string
import xml.etree.ElementTree as et
from xml.dom import minidom

path = 'C:/Python27/Scripts/'

def prettify(elem):
	rough_string = et.tostring(elem, 'utf-8')
	reparsed = minidom.parseString(rough_string)
	return reparsed.toprettyxml()

root = et.Element("namelist")
root.set('version', '1.0')
comment = et.Comment("xml file list generated for javascript use -zhilim")
root.append(comment)

for filename in os.listdir(path):
	if not filename.endswith('.xml'):
		continue
	name = et.SubElement(root, "name")
	name.text = filename

tree = prettify(root)
with open("C:/Python27/Scripts/xmllist.xml", "w") as f:
	f.write(tree)