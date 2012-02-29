import sys
import EUR_2_HRK
import urllib
from xml.dom import minidom

def auth():
    '''The method to do HTTPBasicAuthentication'''
    if len(sys.argv) < 2:
        print "Usage: python " + sys.argv[0] + " currencycode"
        exit()

    currencycode = sys.argv[1]
    _URL = "http://www.petrol.si/api/gas_prices.xml"

    opener = urllib.FancyURLopener()
    f = opener.open(_URL)
    feed = f.read()
    return feed, currencycode

def getChildByAttribute(node, attribute, value):
    for n in node.childNodes:
        if n.attributes[attribute].value == value:
            return n

    return None

def parseXML(xml, currencycode):
    xmldoc = minidom.parseString(xml)
    slovenia = getChildByAttribute(xmldoc.firstChild, 'label', 'Slovenia')
    f95 = getChildByAttribute(slovenia, 'type', '95')
    priceType = getChildByAttribute(f95, 'type', 'normal')
    price = getChildByAttribute(priceType, 'type', 'price')
    return price.firstChild.toxml()

def cijena_EUR(xml, currencycode):
    return float(parseXML(xml, currencycode))

def cijena_HRK(eur):
    return (eur * EUR_2_HRK.getEUR_2_HRK())

if __name__ == "__main__":
    xml, currencycode = auth()
    eur = cijena_EUR(xml, currencycode)
    if currencycode == "EUR":
        print "%.3f" % eur
    else:
        print "%.3f" % cijena_HRK(eur)
