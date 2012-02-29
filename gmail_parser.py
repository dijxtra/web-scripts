## check-gmail.py -- A command line util to check GMail -*- Python -*-
## modified to display mailbox summary for conky

# ======================================================================
# Copyright (C) 2006 Baishampayan Ghose <b.ghose@ubuntu.com>
# Modified 2008 Hunter Loftis <hbloftis@uncc.edu>
# Time-stamp: Mon Jul 31, 2006 20:45+0530
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
# ======================================================================

import sys
import os.path
import datetime
import urllib             # For BasicHTTPAuthentication
import feedparser         # For parsing the feed

_URL = "https://mail.google.com/gmail/feed/atom"
maxlen = 1


def auth():
    '''The method to do HTTPBasicAuthentication'''
    if len(sys.argv) < 3:
        print "Usage: python " + sys.argv[0] + " username password"
        exit()

    uname = sys.argv[1]
    password = sys.argv[2]
    urllib.FancyURLopener.prompt_user_passwd = lambda self, host, realm: (uname, password)

    opener = urllib.FancyURLopener()
    f = opener.open(_URL)
    feed = f.read()
    return feed


def readmail(feed, maxlen):
	'''Parse the Atom feed and print a summary'''
	atom = feedparser.parse(feed)
        yesterday = refresh_count(atom.feed.fullcount)
	print "${color1} %s[%s] unread email(s)" % (atom.feed.fullcount, yesterday)
#	for i in range(min(len(atom.entries), maxlen)):
#		print '          ${color2}%s' % atom.entries[i].title.encode("utf-")
#uncomment the following line if you want to show the name of the sender
#		print '          ${color2}%s' % atom.entries[i].author
#	if len(atom.entries) > maxlen:
#		print ' ${color}more...'

def refresh_count(newcount = None):
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    filename = path + "/gmail_parser.log"

    today = datetime.date.today()
    new_line = str(today) + " " + str(newcount)

    if not os.path.exists(filename):
        f = open(filename, "w")
        f.writelines(new_line)
        f.close()
        return 
        
    f = open(filename, "r+")
    [d, c] = f.read(128).split(" ")
    f.close()

    date = datetime.datetime.strptime(d, "%Y-%m-%d").date()
    count = int(c)

    trend = int(newcount) - count

    if (today - date) > datetime.timedelta(days = 1):
        f = open(filename, "w")
        f.write(new_line)
        f.close()

    return trend

if __name__ == "__main__":
    f = auth()  # Do auth and then get the feed
    readmail(f, int(maxlen)) # Let the feed be chewed by feedparser
