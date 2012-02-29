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
import feedparser         # For parsing the feed
import re

def auth():
    '''The method to do HTTPBasicAuthentication'''

    if len(sys.argv) < 2:
        print "Usage: python " + sys.argv[0] + " username"
        exit()

    uname = sys.argv[1]
    _URL = "http://www.conquerclub.com/rss.php?username=" + uname

    opener = urllib.FancyURLopener()
    f = opener.open(_URL)
    feed = f.read()
    return feed


def readfeed(feed):
	'''Parse the Atom feed and print a summary'''
	atom = feedparser.parse(feed)
        p = re.compile('Game (\d+) Round (\d+) - (\w+) \((\d{2}:\d{2}):\d{2} remaining\)')
        times = []
        for entry in atom.entries:
#            print entry.title
            m = p.match(entry.title)
            if m:
                if m.group(3) == 'READY':
                    times.append(m.group(4))
        if len(times) > 0:
            times.sort()
            p = re.compile('(\d{2}):(\d{2})')
            m = p.match(times[0])
            time = m.group(1) + ":" + m.group(2)
            if len(times) > 1:
                print "%s games ready." % len(times)
            else:
                print "One game ready."
            print "(%s remaining)." % time
        else:
            print "No games ready."


if __name__ == "__main__":
    f = auth()  # Do auth and then get the feed
    readfeed(f) # Let the feed be chewed by feedparser
