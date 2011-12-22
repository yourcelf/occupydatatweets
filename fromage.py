#!/venv/bc/bin/python

#
# Cheese it up.  Run the dev server, and autocompile stuff.
#

import os.path
import subprocess

BASE = os.path.abspath(os.path.dirname(__file__))

app = subprocess.Popen(["python", os.path.join(BASE, "manage.py"), "runserver"])
sass = subprocess.Popen(["compass", "watch"], cwd=os.path.join(BASE, "static", "css", "sass"))

try:
    app.communicate()
except KeyboardInterrupt:
    pass
finally:
    sass.kill()



