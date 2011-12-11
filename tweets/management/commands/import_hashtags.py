import re
import ssl
import socket
import urllib2
import httplib
import logging

from django.core.management import BaseCommand
from django.utils.encoding import force_unicode, DjangoUnicodeDecodeError

from tweets.models import Tweet, HashTag

cache = {}

class Command(BaseCommand):
    args = ''
    help = "Import hashtags from all tweets."

    def handle(self, *args, **kwargs):
        low = int(args[0])
        high = int(args[1])
        chunk = 1000

        for i in range(low, high, 1000):
            print i
            for tweet in Tweet.objects.all()[i:i + chunk]:
                results = re.finditer(r"(#\w+)", tweet.text)
                for match in results:
                    hashtag = match.group(1).lower()
                    if hashtag in cache:
                        tag = cache[hashtag]
                    else:
                        tag, created = HashTag.objects.get_or_create(tag=hashtag)
                        cache[hashtag] = tag
                    tweet.tags.add(tag)
