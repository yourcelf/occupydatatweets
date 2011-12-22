import re

from django.core.management import BaseCommand

from tweets.models import Tweet, HashTag

class Command(BaseCommand):
    args = ''
    help = "Import hashtags from all tweets."

    def handle(self, *args, **kwargs):
        low = int(args[0])
        high = int(args[1])
        chunk = 10000

        for i in range(low, high, chunk):
            print ((i - low) / float(high - low)) * 100
            for tweet in Tweet.objects.all()[i:i + chunk]:
                results = re.finditer(r"(#\w+)", tweet.text)
                for match in results:
                    hashtag = match.group(1).lower()
                    tag, created = HashTag.objects.get_or_create(tag=hashtag)
                    tweet.tags.add(tag)
