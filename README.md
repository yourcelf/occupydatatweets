Occupy Data Twitter Links
=========================

This is a Django site which generates a visualization of links contained in
tweets.  It takes the CSV files from the r-shief OccupyData twitter dumps, extracts
the links, resolves shortened URLs, and presents a visualization of the data.

Here's [example output](http://occupybostonlinks.tirl.org) from the #OccupyBoston hashtag.

Installation
------------

Clone the git repository, then install the dependencies listed in the "requirements.txt" file.  The easiest way to install the dependencies is::

    pip install -r requirements.txt

(You may have to be root).

Next, create the postres database and user, and update the `settings.py` file to reflect your database settings.

Synchronize the database::

    python manage.py syncdb
    python manage.py migrate

Loading data
------------

Put all the un-gzipped CSV files from r-shief's dumps in the `data/` directory, then run the loading command:

    python manage.py import_tweets

Next, resolve the shortened URLs.  Since this is a time-consuming network-bound
operation, you will want to multi-thread it. Use the `multi_import_urls`
management command, with the arguments `start_tweet` (the first tweet to try,
ordered by database ID), `end_tweet` (the last tweet to try), and
`simultaneous_workers` (the numer of daemons to launch which will be making
http requests to resolve URLs.  If you spread this job out on multiple
machines, you may want to specify ranges for each to work from.

    python manage.py multi_import_urls <start_tweet> <end_tweet> <simultaneous_workers>

Next, denormalize the tweet counts, domains, and such.

    python manage.py denormalize_urls

Finally, import some domain categories.  A starting set is defined in
`tweets/management/commands/initial_categories.py`, but you may want to expand
by defining categories for more domains.  Future work is to add a web interface
for this.

    python manage.py initial_categories

Other management commands (Optional)
------------------------------------

Load hashtags from the tweets (which aren't currently used yet, but could be
fun).  Since this is CPU-bound, you probably want to set `simultaneous_workers`
to the number of cores your CPU has:

    python manage.py multi_import_hashtags <simultaneous_workers>

Show the number of tweets/tags/urls/etc. that have been loaded:

    python manage.py count_tweets

Dumping a static site
---------------------

I deployed this as a static site, with the lame script `dump_static_site.py`.
You probably need to tweak the page range for whatever your data set allows.
