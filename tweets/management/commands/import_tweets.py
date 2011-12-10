import os
import re
import csv
import glob
import time
import codecs
import tempfile

from django.core.management import BaseCommand
from django.conf import settings
from django.db import connection, transaction

from tweets.models import Tweet

class Command(BaseCommand):
    args = ''
    help = "Import all the raw tweet data in the data directory."

    def handle(self, *args, **kwargs):
        filenames = glob.glob(os.path.join(settings.BASE, "data/*-raw.csv"))
        with_sizes = sorted([(os.path.getsize(f), f) for f in filenames])
        with_sizes.reverse()
        for size, filename in with_sizes:
            # Fix some brokenness with the csv files...
            print filename, size
            with open(filename, 'rb') as infile:
                with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as outfile:
                    name = outfile.name
                    # Make readable by postgres user so COPY command succeeds
                    # (by default tmpfiles are probably 600)
                    os.system("chmod 644 '%s'" % name)
                    for line in infile:
                        # Clear 0x00 characters that bork postgres -- the seem
                        # to be meant to be newlines
                        newline = line.replace('\x00', '\n')
                        # There're a few tweets in there that escaped differently, ugh
                        newline = re.sub(r'\\"([^,"])', r'""\1', newline)
                        outfile.write(newline)
            cursor = connection.cursor()
            cursor.execute("COPY tweets_tweet (twitter_id, text, profile_image_url, day, hour, minute, created_at, geo, from_user, from_user_id, language, to_user, to_user_id, source) FROM '%s' WITH CSV HEADER DELIMITER AS ',' NULL AS 'N;'" % name)
            transaction.commit_unless_managed()
            os.remove(name)

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self
