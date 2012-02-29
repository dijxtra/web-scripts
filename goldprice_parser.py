import sys
import urllib
from xml.dom import minidom


def auth():
    '''The method to do HTTPBasicAuthentication'''
    if len(sys.argv) < 2:
        print "Usage: python " + sys.argv[0] + " currencycode"
        exit()

    currencycode = sys.argv[1]
    _URL = "http://dgcsc.org/goldprices.xml"

    opener = urllib.FancyURLopener()
    f = opener.open(_URL)
    feed = f.read()
    return feed, currencycode


def parseXML(xml, currencycode):
    xmldoc = minidom.parseString(xml)
    for node in xmldoc.firstChild.childNodes:
        if node.attributes['currencycode'].value == currencycode:
            return node.firstChild.data


if __name__ == "__main__":
    f, currencycode = auth()
    print "%.1f" % float(parseXML(f, currencycode))
