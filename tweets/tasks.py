import re
import logging

from celery.task import task

from tweets.models import Tweet, ShortUrl, CanonicalUrl
from tweets.utils import get_long_url

logger = logging.getLogger(__name__)

link_regex = r"(^|[\n ])(([\w]+?://[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)"

@task
def parse_tweet(tweet_id):
    print tweet_id
    return
    tweet = Tweet.objects.get(pk=tweet_id)
    results = re.finditer(link_regex, tweet.text, re.I | re.DOTALL)
    for match in results:
        short_url = match.group(2).split("&")[0]
        # Retry transaction
        try:
            url = ShortUrl.objects.get(short=short_url).url
        except ShortUrl.DoesNotExist:
            # This is blocking and long (waiting for network)
            long_url = get_long_url(short_url)
            url, created = CanonicalUrl.objects.get_or_create(
                url=long_url
            )
            # Use get_or_create because another thread might have created it
            # while we were getting the long url.
            ShortUrl.objects.get_or_create(
                short=short_url,
                url=url
            )
        finally:
            tweet.urls.add(url)
