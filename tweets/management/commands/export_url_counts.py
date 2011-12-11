import codecs

from django.core.management import BaseCommand
from django.db.models import Count

from tweets.models import CanonicalUrl
from tweets.utils import UnicodeWriter

class Command(BaseCommand):
    args = '<outputfile>'
    help = "Export all URLs and counts, ordered by count."

    def handle(self, *args, **kwargs):
        with open(args[0], 'w') as fh:
            writer = UnicodeWriter(fh)
            for can in CanonicalUrl.objects.annotate(
                    count=Count('tweet')).order_by('-count'):
                writer.writerow([unicode(can.count), can.url])
        
