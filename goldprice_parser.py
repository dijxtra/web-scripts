import sys
import urllib
from xml.dom import minidom
import re

currencycode = sys.argv[1]

_URL = "http://dgcsc.org/goldprices.xml"

def auth():
    '''The method to do HTTPBasicAuthentication'''
    opener = urllib.FancyURLopener()
    f = opener.open(_URL)
    feed = f.read()
    return feed


def parseXML(xml):
    xmldoc = minidom.parseString(xml)
    for node in xmldoc.firstChild.childNodes:
        if node.attributes['currencycode'].value == currencycode:
            return node.firstChild.data


if __name__ == "__main__":
    f = auth()
    print "%.1f" % float(parseXML(f))
