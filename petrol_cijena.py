import sys
import EUR_2_HRK
import urllib
from xml.dom import minidom

def auth():
    '''The method to do HTTPBasicAuthentication'''
    if len(sys.argv) < 3:
        print "Usage: python " + sys.argv[0] + " country currencycode"
        exit()

    country = sys.argv[1]
    currencycode = sys.argv[2]
    _URL = "http://www.petrol.si/api/gas_prices.xml"

    opener = urllib.FancyURLopener()
    f = opener.open(_URL)
    feed = f.read()
    return feed, country, currencycode

def map_country_code(country_code):
    if country_code == 'HR':
        return 'Croatia'
    elif country_code == 'SI':
        return 'Slovenia'
    return None

def getChildByAttribute(node, attribute, value):
    for n in node.childNodes:
        if n.attributes[attribute].value == value:
            return n

    return None

def parseXML(xml, country):
    xmldoc = minidom.parseString(xml)
    slovenia = getChildByAttribute(xmldoc.firstChild, 'label', country)
    f95 = getChildByAttribute(slovenia, 'type', '95')
    priceType = getChildByAttribute(f95, 'type', 'normal')
    price = getChildByAttribute(priceType, 'type', 'price')
    return price.firstChild.toxml()

def cijena(xml, country):
    return float(parseXML(xml, country))

if __name__ == "__main__":
    xml, country, currencycode = auth()
    base_price = float(cijena(xml, map_country_code(country)))
    if (country, currencycode) == ('HR', 'HRK'):
        print "%.2f" % base_price
    elif (country, currencycode) == ('HR', 'EUR'):
        print "%.2f" % (base_price / EUR_2_HRK.getEUR_2_HRK())
    elif (country, currencycode) == ('SI', 'HRK'):
        print "%.2f" % (base_price * EUR_2_HRK.getEUR_2_HRK())
    elif (country, currencycode) == ('SI', 'EUR'):
        print "%.2f" % base_price
