#!/usr/bin/env python
import os
import json

BASE = os.path.abspath(os.path.dirname(__file__))
OUT = os.path.join(BASE, "..", "out")

def build_url_pages():
    with open(os.path.join(BASE, "..", "static", "data", "pixel-count.json")) as fh:
        data = json.load(fh)

    for thing in data:
        tweet_id = thing[4]
        path = "url/{0}/".format(tweet_id)
        out = os.path.join(OUT, path)
        try:
            os.makedirs(out)
        except OSError:
            pass
        os.system("curl -L http://localhost:8000/{0} > {1}/index.html".format(path, out))
    
def build_pixel_pages():
    for sort in ["date", "count"]:
        path = "pixel/%s" % sort
        out = os.path.join(OUT, path)
        try:
            os.makedirs(out)
        except OSError:
            pass
        os.system("curl -L http://localhost:8000/{0} > {1}/index.html".format(path, out))

def copy_static():
    os.system("rsync -a --delete {0} {1}".format(
        os.path.join(BASE, "..", "static").rstrip("/") + "/",   
        os.path.join(OUT, "static").rstrip("/") + "/",
    ))

if __name__ == "__main__":
    build_url_pages()
    build_pixel_pages()
    copy_static()
