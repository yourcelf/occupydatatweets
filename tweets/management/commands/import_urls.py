import re
import logging

from django.core.management import BaseCommand
from django.utils.encoding import force_unicode, DjangoUnicodeDecodeError
from django.db.utils import DatabaseError

from tweets.models import Tweet, ShortUrl, CanonicalUrl
from tweets.utils import get_long_url
from django.db import transaction

logger = logging.getLogger(__name__)

link_regex = r"(^|[\n ])(([\w]+?://[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)"

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

        chunk = 1000

        for x in range(low, high, chunk):
            print x, "/", (high), (float(x - low) / (high - low)) * 100
            for tweet in Tweet.objects.all()[x:x + chunk]:
                results = re.finditer(link_regex, tweet.text, re.I | re.DOTALL)
                for match in results:
                    short_url = match.group(2).split("&")[0]
                    try:
                        url = ShortUrl.objects.get(short=short_url).url
                    except ShortUrl.DoesNotExist:
                        url, created = CanonicalUrl.objects.get_or_create(url=get_long_url(short_url))
                        ShortUrl.objects.get_or_create(
                            short=short_url,
                            url=url,
                        )
                    #print tweet.pk, ":", short_url, "=>", url
                    #print tweet.pk
                    tweet.urls.add(url)
