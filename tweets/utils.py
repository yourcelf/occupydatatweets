import csv
import ssl
import socket
import urllib2
import httplib
import codecs
import cStringIO

from django.utils.encoding import force_unicode

link_regex = r"(^|[\n ])(([\w]+?://[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)"

class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"

class RawRedirectHandler(urllib2.HTTPRedirectHandler):
    def get_redirect(self, req, fp, code, msg, headers):
        loc = headers['Location']
        status = code
        return loc, status
    def http_error_301(self, *a, **k): return self.get_redirect(*a, **k)
    def http_error_302(self, *a, **k): return self.get_redirect(*a, **k)
    def http_error_307(self, *a, **k): return self.get_redirect(*a, **k)


def get_long_url(short_url):
    url = short_url
    opener = urllib2.build_opener(RawRedirectHandler())
    status = 0
    while status != 200:
        request = HeadRequest(url)
        try:
            url, status = opener.open(request, timeout=1)
            url = force_unicode(url)
            #print "..........  ", url
        except (KeyError, ValueError, urllib2.HTTPError, socket.timeout, ssl.SSLError, urllib2.URLError, httplib.BadStatusLine):
            break
    return url

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
