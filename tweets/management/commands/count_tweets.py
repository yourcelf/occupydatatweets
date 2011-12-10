from django.core.management import BaseCommand

from tweets.models import Tweet

class Command(BaseCommand):
    args = ''
    help = "Display number of tweets in db."

    def handle(self, *args, **kwargs):
        print Tweet.objects.count()
