import ssl
import socket
import codecs
import urllib2
import httplib
import logging
from django.utils.encoding import force_unicode

from django.core.management import BaseCommand

logger = logging.getLogger(__name__)

class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"

class RawRedirectHandler(urllib2.HTTPRedirectHandler):
    def get_redirect(self, req, fp, code, msg, headers):
        loc = headers.get('Location', "")
        status = code
        return loc, status
    def http_error_301(self, *a, **k): return self.get_redirect(*a, **k)
    def http_error_302(self, *a, **k): return self.get_redirect(*a, **k)
    def http_error_307(self, *a, **k): return self.get_redirect(*a, **k)

def get_long_url(short_url):
    url = short_url
    url = url.split("&")[0]
    opener = urllib2.build_opener(RawRedirectHandler())
    status = 0
    while status != 200:
        request = HeadRequest(url)
        try:
            url, status = opener.open(request, timeout=1)
            url = force_unicode(url)
            #print "..........  ", url
        except (ValueError, urllib2.HTTPError, socket.timeout, ssl.SSLError, urllib2.URLError, httplib.BadStatusLine, httplib.InvalidURL):
            break
        except Exception as e:
            logger.error(short_url)
            logger.error(url)
            logger.exception(e)
            break
    return url

class Command(BaseCommand):
    args = '<infile> <outfile>'
    help = "Expand shortened urls in infile, write results as tab-separated values to outfile."

    def handle(self, *args, **kwargs):
        with codecs.open(args[0], 'r', 'utf-8') as infile:
            with codecs.open(args[1], 'w', 'utf-8') as outfile:
                for i,line in enumerate(infile):
                    parts = line.split("\t")
                    if len(parts) > 1:
                        outfile.write(line)
                    else:
                        outfile.write(line.strip())
                        outfile.write("\t")
                        outfile.write(get_long_url(line).strip())
                        outfile.write("\n")
