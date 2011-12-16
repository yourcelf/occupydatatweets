import os
import subprocess

from django.core.management import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    args = '<low> <high> <num_workers>'
    help = "Parse the URLs from all tweets as quickly as possible."

    def handle(self, *args, **kwargs):
        low = int(args[0])
        high = int(args[1])
        workers = int(args[2])
        
        chunk = (high - low) / workers
        procs = []
        try:
            for i in range(low, high, chunk):
                proc = subprocess.Popen(["python", os.path.join(settings.BASE, "manage.py"), 
                    "import_urls", str(i), str(i + chunk)])
                procs.append(proc)

            while True:
                try:
                    procs.pop().communicate()
                except IndexError:
                    break
        except KeyboardInterrupt:
            for proc in procs:
                proc.kill()
