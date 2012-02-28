import sys
import EUR_2_HRK
import fetch
from lxml.cssselect import CSSSelector #nocov
from lxml import etree

try:
    currencycode = sys.argv[1]
except IndexError:
    currencycode = ""

_URL = "http://www.ina.hr/default.aspx?id=203"
_benzin = "INA Eurosuper BS 95"

def parseHTML():
    p = fetch.HTMLpage(_URL)
    p.fetch_page()

    parent = None
    span_sel = CSSSelector('span')
    for s in span_sel(p.root):
        text = s.text.replace(unichr(160), ' ').strip(' ').replace('  ', ' ')
#        print text
        if text == _benzin:
            parent = s.getparent().getparent()
            break

    if parent is None:
        raise Exception('Trazeni bezin nije pronadjen.')

    price_sel = CSSSelector('tr > td[style="text-align: right;"] > strong')
    try:
        price = price_sel(parent)[0]
    except IndexError:
        raise Exception('Selector za cijenu benzina ne daje rezultat.')

    return float(price.text.replace(',', '.'))

def cijena_HRK():
    return float(parseHTML())

def cijena_EUR():
    return (cijena_HRK() / EUR_2_HRK.getEUR_2_HRK())

if __name__ == "__main__":
    if currencycode == "EUR":
        print "%.3f" % cijena_EUR()
    else:
        print "%.3f" % cijena_HRK()
