import os
import glob
import tempfile
import subprocess

from django.core.management import BaseCommand
from django.conf import settings

MANAGE = os.path.join(settings.BASE, "manage.py")

class Command(BaseCommand):
    args = "<num_simultaneous_workers> <input_dir> <output_dir>"
    help = "(Relatively) Quickly import all the urls from all tweets."

    def handle(self, num_simultaneous_workers, *args, **kwargs):
        num_simultaneous_workers = int(num_simultaneous_workers)
        in_tmp_dir = args[0] if args else tempfile.mkdtemp(prefix=os.path.join(settings.BASE, "data", "shorturls_"))
        out_tmp_dir = args[1] if args else tempfile.mkdtemp(prefix=os.path.join(settings.BASE, "data", "longurls_"))
        if args:
            print "Using given directory '%s'" % in_tmp_dir
        else:
            print "Extracting short urls from all tweets to '%s'.." % in_tmp_dir
            proc = subprocess.Popen(["python", MANAGE, "extract_short_urls", in_tmp_dir])
            proc.wait()

        queue = glob.glob(os.path.join(in_tmp_dir, '*.csv'))
        procs = []
        while queue:
            infile = queue.pop()
            outfile = os.path.join(out_tmp_dir, os.path.basename(infile))
            if os.path.exists(outfile):
                with open(infile) as fh1:
                    with open(outfile) as fh2:
                        if len(infile.read().split("\n")) == \
                                len(outfile.read().split("\n")):
                            print "Looks like '%s' is already complete." % outfile
                            continue
            
            print "Starting worker for %s => %s." % (infile, outfile)
            proc = subprocess.Popen(["python", MANAGE, "justurls", infile, outfile])
            procs.append(proc)
            while queue and len(procs) == num_simultaneous_workers:
                procs[0].wait()
                procs.pop()
        while procs:
            procs[0].wait()
            procs.pop()

        print "Loading shortened urls back into the database."
        for filename in glob.glob(os.path.join(out_tmp_dir, '*.csv')):
            proc = subprocess.Popen(["python", MANAGE, "load_just_urls", filename])
            proc.wait()
