#!/usr/bin/env python
import os

for p in range(1, 19):
    for sort in ["date", "count"]:
        out = "out/%s/%s/" % (p, sort)
        try:
            os.makedirs(out)
        except OSError:
            pass
        os.system("curl -L http://localhost:8000/%s/%s/ > %sindex.html" % (p, sort, out))
os.system("curl -L http://localhost:8000/ > out/index.html")
