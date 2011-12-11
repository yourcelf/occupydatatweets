import os
import subprocess

from django.core.management import BaseCommand
from django.conf import settings

from tweets.models import Tweet

class Command(BaseCommand):
    args = ''
    help = "Display number of tweets in db."

    def handle(self, *args, **kwargs):
        workers = int(args[0])

        low = 0
        high = Tweet.objects.count()
        chunk = high / workers
        procs = []
        try:
            for worker in range(0, workers):
                low = chunk * worker
                high = low + chunk
                proc = subprocess.Popen(["python", os.path.join(settings.BASE, "manage.py"), "import_hashtags", str(low), str(high)])
                procs.append(proc)

            while True:
                try:
                    procs.pop().wait()
                except IndexError:
                    break
        except KeyboardInterrupt:
            for proc in procs:
                proc.kill()
