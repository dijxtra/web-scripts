import sys
import fetch
import feedparser
import re

def parseRSS(URL):
    p = fetch.HTMLpage(URL)
    p.fetch_page()

    atom = feedparser.parse(p.raw())
    p = re.compile('Rating: \d+<br />Time Left: ((?:\d+ days? \d+ hours?)|(?:1 day)|(?:\d+ hours? \d+ minutes?))( )?<br />Move #: \d+')
    times = []
    for entry in atom.entries:
        m = p.match(entry.description)
        if m:
            times.append(m.group(1))
    if len(atom.entries) > 0:
#        times.sort()
#        p = re.compile('(\d{2}):(\d{2})')
#        m = p.match(times[0])
#        time = m.group(1) + ":" + m.group(2)
        if len(atom.entries) > 1:
            print "%s games ready." % len(atom.entries)
        else:
            print "One game ready."
        print "(%s remaining)." % times[0]
    else:
        print "No games ready."


if __name__ == "__main__":
    uname = sys.argv[1]
    URL = "http://www.chess.com/rss/echess/" + uname
    parseRSS(URL)
