import codecs

from django.core.management import BaseCommand
from tweets.models import ShortUrl, CanonicalUrl

class Command(BaseCommand):
    args = '<infile>'
    help = "Load the <short_url>TAB<long_url> pairs from the given file."

    def handle(self, *args, **kwargs):
        with codecs.open(args[0]) as fh:
            for i, line in enumerate(fh):
                print i
                parts = line.split("\t")
                if len(parts) > 1:
                    curl, created = CanonicalUrl.objects.get_or_create(url=parts[1])
                    try:
                        surl = ShortUrl.objects.get(short=parts[0])
                        surl.url = curl
                        surl.save()
                    except surl.DoesNotExist:
                        surl = ShortUrl.objects.create(short=parts[0], url=curl)
