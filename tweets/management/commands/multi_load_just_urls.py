import os
import glob
import subprocess

from django.core.management import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    args = '<in_directory> <num_workers>'
    help = "Parse the URLs from all tweets as quickly as possible."

    def handle(self, *args, **kwargs):
        in_dir, num_workers = args
        num_workers = int(num_workers)

        files = sorted(glob.glob(os.path.join(in_dir, "*.csv")))
        procs = []

        while files:
            while True:
                if len(procs) < num_workers:
                    proc = subprocess.Popen(["python", os.path.join(settings.BASE, "manage.py"), 
                            "load_just_urls", files.pop()])
                    procs.append(proc)
                    continue
                else:
                    try:
                        procs.pop().wait()
                    except IndexError:
                        break
