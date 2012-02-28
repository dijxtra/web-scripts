## check-conquerclub.py -- A command line util to check for ready Conquer Club games by Nikola Skoric
## Based on check-gmail.py by Baishampayan Ghose

# ======================================================================
# Copyright (C) 2006 Baishampayan Ghose <b.ghose@ubuntu.com>
# Modified 2009 Nikola Skoric <nskoric@gmail.com>
# Time-stamp: Wed Nov 18 18:12:26 CET 2009
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
# ======================================================================

import sys
import urllib             # For BasicHTTPAuthentication
from xml.dom import minidom
import re

currencycode = "HRK"

_URL = "http://www.ecb.int/stats/eurofxref/eurofxref-daily.xml"

def auth():
    '''The method to do HTTPBasicAuthentication'''
    opener = urllib.FancyURLopener()
    f = opener.open(_URL)
    feed = f.read()
    return feed


def parseXML(xml):
    xmldoc = minidom.parseString(xml)
    for node in xmldoc.getElementsByTagName('Cube'):
        try:
            if node.attributes['currency'].value == currencycode:
                return node.attributes['rate'].value
        except:
            pass
    return None

def getEUR_2_HRK():
    f = auth()  # Do auth and then get the feed
    return float(parseXML(f))


if __name__ == "__main__":
    print "%.3f" % getEUR_2_HRK()
