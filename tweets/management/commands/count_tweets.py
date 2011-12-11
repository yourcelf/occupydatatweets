from django.core.management import BaseCommand

from tweets.models import Tweet, ShortUrl, CanonicalUrl, HashTag
from tweets.utils import UnicodeWriter

class Command(BaseCommand):
    args = ''
    help = "Display number of tweets in db."

    def handle(self, *args, **kwargs):
        print Tweet.objects.count(), "Tweets",
        print ShortUrl.objects.count(), "Short URLs"
        print CanonicalUrl.objects.count(), "Canonical URLs"
        print HashTag.objects.count(), "Tags"
