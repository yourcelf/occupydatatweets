import re

from django.core.management import BaseCommand
from tweets.models import Tweet
from tweets.tasks import parse_tweet

class Command(BaseCommand):
    args = 'requires two integers: the range of tweets to scan.'
    help = "Queues tweets to be parsed by AMQP worker"

    def handle(self, *args, **kwargs):
        try:
            low = int(args[0])
            high = int(args[1])
        except (ValueError, IndexError):
            print self.args
            return

        for tweet_id in Tweet.objects.all().values_list(
                'pk', flat=True)[low:high]:
            parse_tweet.delay(tweet_id)
