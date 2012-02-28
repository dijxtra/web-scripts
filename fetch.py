"""
Fetch
=====

Metods and classes for fetching HTML pages.
"""
import urllib, urllib2 #nocov
from StringIO import StringIO #nocov
import hashlib #nocov
import os #nocov
from lxml import etree #nocov

# build opener with HTTPCookieProcessor
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
urllib2.install_opener(opener)

class PageDoesNotExist(Exception):
    """Exception raised when there is a HTTPError 404"""
    def __init__(self, URL):
        self.value = URL + " doesn't exist, check your server URL."

    def __str__(self):
        return repr(self.value)

def fetch_page(URL, posts = None, last_modified = None):
    """A simple HTTP fetcher.

    Requests a web page on given URL. Optional posts argument takes dictionary of values to be sent by POST method. If last_modified argument is defined, If-Modified-Since header is sent to web server.

    Return value of urllib2.urlopen is returned.
    """
#    print "Fetching " + URL

    request = urllib2.Request(URL)
    request.add_header('User-Agent','Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.19) Gecko/2010040116 Ubuntu/9.04 (jaunty) Firefox/3.0.19')
    if posts is not None:
        request.add_data(urllib.urlencode(posts))

    if last_modified is not None:
        request.add_header('If-Modified-Since', last_modified)

    try:
        response = opener.open(request)
    except urllib2.HTTPError as e:
        if e.code == 404:
            raise PageDoesNotExist(URL)
        else:
            raise e

    return response

def fetch_if_modified_since(URL, last_modified):
    """Fetched a web page if modified since given Last-Modified using fetch_page method."""
    try:
        return fetch_page(URL, posts = None, last_modified = last_modified)
    except urllib2.HTTPError as e:
        if e.code == 304:
            return None

def get_tree_from_response(response):
    """Converts urllib2.urlopen return value to etree.ElementTree object"""
    if response is None:
        return ""

    parser = etree.HTMLParser()
    root = etree.parse(StringIO(response.read()), parser)
       
    return root


class HTMLpage:
    """Retrieves and stores a HTML page. Has basic cashing support."""
    last_modified = ''
    url = ''
    root = None
    filename = ''
    from_cache = False
    
    def __init__(self, url = ''):
        """Constructor takes page URL."""
        self.url = url
        
        return

    def parse_response(self, response):
        """Filles in class properties with data from response and saves page in cache."""
        if response is None:
            return

        self.url = response.url
        self.last_modified = response.headers.get('Last-Modified')

        self.filename = hashlib.sha1(self.url).hexdigest() + '.html'

        self.root = get_tree_from_response(response)

        self.from_cache = False

        if self.last_modified is not None:
            self.save()
        
        return

    def get_page(self, posts = None):
        """Gets a page from cache or from web if cache is old."""
        if (posts is not None) or (not self.is_in_cache()):
            response = self.fetch_page(posts)
            self.parse_response(response)
            return
        
        response = fetch_if_modified_since(self.url, self.last_modified)
        if response is not None:
            self.parse_response(response)
        else:
            self.get_from_cache()
        
        return

    def fetch_page(self, posts = None):
        """Gets a page from web."""
        response = fetch_page(self.url, posts = posts)
        self.parse_response(response)
        return
        

    def html(self):
        """Returns HTML of the page."""
        return etree.tostring(self.root, pretty_print=True) #I need sane HTML

    def raw(self):
        """Returns source of the page."""
        return etree.tostring(self.root)

    def is_in_cache(self):
        """Checks if cached version of the page exists."""
        try:
            f = open('cache/index.txt', 'r+')
            lines = f.readlines()
            f.close()
        except IOError:
            lines = []

        for l in lines:
            if l.split(" ")[1] == self.url:
                return True

        return False

    def get_index(self):
        """Parses cache index file. Returns its contents in a list."""
        try:
            f = open('cache/index.txt', 'r+')
            lines = f.readlines()
            f.close()
        except IOError:
            lines = []
        return lines


    def get_from_cache(self):
        """Gets the page from cache."""
#        print "Getting from cache: " + self.url
        lines = self.get_index()

        for l in lines:
            [f, u, t] = l.split(" ", 2)
            if u == self.url:
                self.filename = f.strip("\n")
                self.last_modified = t.strip("\n")

        f = open('cache/' + self.filename, 'r')

        self.root = get_tree_from_response(f)
        self.from_cache = True

        return

    def save(self):
        """Saves HTML to cache if this version is not in cache."""
        lines = self.get_index()
        for l in lines:
            [f, u, t] = l.split(" ", 2)
            if u == self.url:
                lines.remove(l)

        lines.append(unicode(self.filename) + ' ' + unicode(self.url) + ' ' + unicode(self.last_modified) + "\n")

        if not os.access('cache', os.F_OK):
            os.mkdir('cache')

        f = open('cache/index.txt', 'w')
            
        for l in lines:
            f.write(l)
        f.close()

        f = open('cache/' + self.filename, 'w')
        f.write(self.raw())
        f.close()

        return

    def clear_cache(self):
        """Removes this page from cache."""
        lines = self.get_index()
        files = []
        for l in lines:
            [f, u, t] = l.split(" ", 2)
            if u == self.url:
                lines.remove(l)
                files.append(f)

        f = open('cache/index.txt', 'w')
        for l in lines:
            f.write(l)
        f.close()

        for f in files:
            os.remove('cache/' + f)

        return


    def __str__(self):
        """Prints out content of the object in multiline form."""
        retval = ""

        retval += "URL: " + self.url + "\n"
        retval += "Last-Modified: " + unicode(self.last_modified) + "\n"
        retval += "Filename: " + self.filename + "\n"
        retval += "From cache? " + unicode(self.from_cache) + "\n"

        return retval
