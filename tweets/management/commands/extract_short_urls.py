import os
import re
import codecs

from django.core.management import BaseCommand

from tweets.models import ShortUrl, Tweet

link_regex = r"(^|[\n ])(([\w]+?://[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)"

class Command(BaseCommand):
    args = '<outdir>'
    help = "Extracts all short urls, and long urls, into a tab-separated single file."

    def handle(self, *args, **kwargs):
        shorts = set()


        total = Tweet.objects.count()
        chunk = 100000
        count = 0
        def new_fh(fh, count, chunk):
            if fh is not None:
                fh.close()
            fh = codecs.open(os.path.join(args[0], "%04d.csv" % (count / chunk)), 
                    'w', 'utf-8')
            return fh
        fh = new_fh(None, count, chunk)
        for surl in ShortUrl.objects.all().select_related('url'):
            fh.write(surl.short)
            fh.write("\t")
            fh.write(surl.url.url)
            fh.write("\n")
            shorts.add(surl.short)
            count += 1
            if count % chunk == 0:
                fh = new_fh(fh, count, chunk)
        for i in range(0, total, chunk):
            print i/chunk, "/", total/chunk
            for tweet in Tweet.objects.all().values_list('text', flat=True)[i:i+chunk]:
                results = re.finditer(link_regex, tweet, re.I | re.DOTALL)
                for match in results:
                    short_url = match.group(2)
                    if short_url not in shorts:
                        fh.write(short_url)
                        fh.write("\n")
                        shorts.add(short_url)
                count += 1
                if count % chunk == 0:
                    fh = new_fh(fh, count, chunk)
