import sys
import EUR_2_HRK
import fetch
from lxml.cssselect import CSSSelector #nocov
from lxml import etree

try:
    currencycode = sys.argv[1]
except IndexError:
    currencycode = ""

_URL = "http://www.omv.si/portal/01/si/!ut/p/c5/04_SB8K8xLLM9MSSzPy8xBz9CP0os3hfA0sPN89Qo1BHE3dvCzdzCx8vAwgAykeiyBsZeJt6hzkawuTx6w4uztH388jPTdUvyI0oBwBJKenZ/dl3/d3/L2dJQSEvUUt3QS9ZQnZ3LzZfTTA5SEZJVTJVQTRHSzhGN0gxTDAwMDAwMDA!/"
_benzin = "OMV Carrera 95"
    
def parseHTML():
    p = fetch.HTMLpage(_URL)
    p.fetch_page()

    head_sel = CSSSelector('body table > tbody tr > td')
    for h in head_sel(p.root):
        if h.text is None:
            continue
        text = h.text.replace(unichr(160), ' ').strip(' ')
        if text == _benzin:
            parent = h.getparent()
            break

    if parent is None:
        return

    price_sel = CSSSelector('td')
    price = price_sel(parent)[1]

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
