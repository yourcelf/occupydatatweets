import re
import ssl
import socket
import urllib2
import httplib
import logging

from django.core.management import BaseCommand
from django.utils.encoding import force_unicode, DjangoUnicodeDecodeError

from tweets.models import Tweet, ShortUrl, CanonicalUrl

link_regex = r"(^|[\n ])(([\w]+?://[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)"
logger = logging.getLogger(__name__)

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
        except (ValueError, urllib2.HTTPError, socket.timeout, ssl.SSLError, urllib2.URLError, httplib.BadStatusLine, httplib.InvalidURL):
            break
        except Exception as e:
            logger.error(short_url)
            logger.error(url)
            logger.exception(e)
            break
    return url

class Command(BaseCommand):
    args = 'requires two integers: the range of tweets to scan.'
    help = "Parse the URLs from all tweets"

    def handle(self, *args, **kwargs):
        try:
            low = int(args[0])
            high = int(args[1])
        except (ValueError, IndexError):
            print self.args
            return

        chunk = 100

        for x in range(low, high, chunk):
            if x % 1000 == 0:
                print x, "/", (high), (float(x) / high)
            for tweet in Tweet.objects.all()[x:x + chunk]:
                results = re.finditer(link_regex, tweet.text, re.I | re.DOTALL)
                for match in results:
                    short_url = match.group(2).split("&")[0]
                    try:
                        url = ShortUrl.objects.get(short=short_url).url
                    except ShortUrl.DoesNotExist:
                        url, created = CanonicalUrl.objects.get_or_create(url=get_long_url(short_url))
                        ShortUrl.objects.create(
                            short=short_url,
                            url=url,
                        )
                    #print tweet.pk, ":", short_url, "=>", url
                    #print tweet.pk
                    tweet.urls.add(url)
