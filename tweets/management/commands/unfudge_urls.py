import re
import urlparse

from django.core.management import BaseCommand
from django.db import connection, transaction

from tweets.models import Tweet, ShortUrl, CanonicalUrl, Domain

cache = {}

class Command(BaseCommand):
    args = ''
    help = "ARGGGGHH!!!!!!!!!!!!"

    def handle(self, *args, **kwargs):
        cursor = connection.cursor()
        print "Clearing Tweet / CanonicalUrl join table"
        cursor.execute("""DELETE FROM tweets_tweet_urls""")
        transaction.commit_unless_managed()

        print "Normalizing canonical urls"
        qs = CanonicalUrl.objects.filter(url__contains="\n").order_by('-tweet_count')
        total = qs.count()
        for i, url in enumerate(qs):
            print i, url.tweet_count, (float(i) / total * 100)
            stripped = url.url.strip()
            try:
                clean_url = CanonicalUrl.objects.get(url=stripped)
            except CanonicalUrl.DoesNotExist:
                url.url = stripped
                url.save()
                pass
            else:
                url.shorturl_set.all().update(url=clean_url)
                pass
