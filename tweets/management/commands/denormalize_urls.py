import re
import urlparse

from django.core.management import BaseCommand
from django.db import connection, transaction

from tweets.models import Tweet, ShortUrl, CanonicalUrl, Domain

cache = {}

class Command(BaseCommand):
    args = ''
    help = "Denormalize the number of tweets which refer to each URL."

    def handle(self, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute("""UPDATE tweets_canonicalurl c 
            SET tweet_count = (SELECT COUNT(t.id) FROM 
                tweets_tweet_urls t WHERE t.canonicalurl_id = c.id)
        """)
        for can in CanonicalUrl.objects.all():
            domain_str = urlparse.urlparse(can.url).netloc.strip().lower()
            domain_str = re.sub('^www\.', '', domain_str)
            can.first_appearance = can.tweet_set.order_by('created_at')[0].created_at
            if domain_str in cache:
                domain = cache[domain_str]
            else:
                domain, created = Domain.objects.get_or_create(domain=domain_str)
                cache[domain_str] = domain
            can.domain = domain
            can.save()
        transaction.commit_unless_managed()

