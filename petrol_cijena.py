import sys
import EUR_2_HRK
import fetch
from lxml.cssselect import CSSSelector #nocov
from lxml import etree

try:
    currencycode = sys.argv[1]
except IndexError:
    currencycode = ""

_URL = "http://www.petrol.si/index.php?sv_path=98,104"
_benzin = "Petrol 95"

def parseHTML():
    p = fetch.HTMLpage(_URL)
    p.fetch_page()

    head_sel = CSSSelector('h3 > a')
    for h in head_sel(p.root):
        if h.text == _benzin:
            parent = h.getparent().getparent()
            break

    if parent is None:
        return

    price_sel = CSSSelector('div.gibanje_cen > div > div.gibanje_cen_vrednost > strong')
    price = price_sel(parent)[0]

    return float(price.text.replace(',', '.'))

def cijena_EUR():
    return float(parseHTML())

def cijena_HRK():
    return (cijena_EUR() * EUR_2_HRK.getEUR_2_HRK())

if __name__ == "__main__":
    if currencycode == "EUR":
        print "%.3f" % cijena_EUR()
    else:
        print "%.3f" % cijena_HRK()
