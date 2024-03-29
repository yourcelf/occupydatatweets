from django.core.management import BaseCommand

from tweets.models import Domain

class Command(BaseCommand):
    args = ''
    help = "Load initial domain categories."

    def handle(self, *args, **kwargs):
        for categories in initial_categories:
            domain, created = Domain.objects.get_or_create(domain=categories[0])
            domain.category = categories[1]
            if len(categories) == 3:
                domain.subcategory = categories[2]
            domain.save()


# Culled from https://docs.google.com/spreadsheet/ccc?key=0AvqikmfupFMYdFF2bkFaY180ZkVWbWNnbXJhamYwZGc#gid=0
initial_categories = [
    ('youtube.com','video'),
    ('twitpic.com','image'),
    ('twitter.com','tweet'),
    ('flickr.com','image'),
    ('yfrog.com','image'),
    ('occupyboston.org','occupy'),
    ('livestream.com','stream'),
    ('','fail'),
    ('ow.ly','fail'),
    ('ustream.tv','stream'),
    ('boston.com','news'),
    ('blog.thephoenix.com','news'),
    ('bit.ly','fail'),
    ('lockerz.com','other','sharing'),
    ('t.co','fail'),
    ('instagr.am','image'),
    ('twitvid.com','video'),
    ('bostonherald.com','news'),
    ('dailykos.com','blog'),
    ('facebook.com','fb'),
    ('metro.us','news'),
    ('guardian.co.uk','news'),
    ('thinkprogress.org','blog'),
    ('m.facebook.com','fb'),
    ('bostonglobe.com','news'),
    ('twitlonger.com','fail'),
    ('paper.li','blog'),
    ('huffingtonpost.com','blog'),
    ('privacysos.org','blog'),
    ('bostinno.com','blog'),
    ('twitgoo.com','image'),
    ('occupybucharest.com','occupy'),
    ('wepay.com','donation'),
    ('biggovernment.com','blog'),
    ('thephoenix.com','news'),
    ('aclum.org','blog'),
    ('reddit.com','blog','aggregator'),
    ('openmediaboston.org','news'),
    ('globalrevolution.tv','stream'),
    ('foursquare.com','geo','geo'),
    ('sites.google.com','google'),
    ('l2.yimg.com','image'),
    ('rawstory.com','news'),
    ('myfoxboston.com','news'),
    ('www10.nytimes.com','news'),
    ('wbur.org','news'),
    ('justin.tv','stream'),
    ('anonops.blogspot.com','blog'),
    ('rightnow.io','blog'),
    ('livestre.am','stream'),
    ('thebostonchannel.com','blog'),
    ('homelandsecuritynewswire.com','blog'),
    ('thenation.com','news'),
    ('articles.boston.com','news'),
    ('en.wikipedia.org','wikipedia'),
    ('wired.com','blog'),
    ('boston.cbslocal.com','news'),
    ('therightsphere.com','blog'),
    ('www1.whdh.com','blog'),
    ('patdollard.com','blog'),
    ('i.imgur.com','image'),
    ('bluemassgroup.com','blog'),
    ('occupywallst.org','occupy'),
    ('digboston.com','news'),
    ('mypict.me','image'),
    ('universalhub.com','blog'),
    ('vimeo.com','video'),
    ('paulfetch.com','blog'),
    ('zerohedge.com','blog'),
    ('wsws.org','blog'),
    ('shar.es','fail'),
    ('veteransforpeace.org','blog','veterans'),
    ('whitehonor.com','blog','hate'),
    ('businessinsider.com','blog','business'),
    ('washingtonpost.com','blog'),
    ('futureofcapitalism.com','news'),
    ('occupybostonglobe.com','occupy'),
    ('fireandreamitchell.com','blog'),
    ('michaelgraham.com','blog'),
    ('cbsnews.com','news'),
    ('bpdnews.com','blog','police'),
    ('socialismartnature.tumblr.com','blog'),
    ('storyful.com','blog'),
    ('newyorker.com','news'),
    ('cdn.livestream.com','stream'),
    ('wearethe99percent.tumblr.com','blog'),
    ('tennessean.com','news'),
    ('accounts.google.com','google'),
    ('someecards.com','other','cards'),
    ('truth-out.org','blog'),
    ('pastebin.com','other','text'),
    ('reuters.com','news'),
    ('theatlantic.com','news'),
    ('docs.google.com','google'),
    ('commondreams.org','news'),
    ('mlnurl.com','fail'),
    ('alternet.org','news'),
    ('radioreference.com','other','radioequipment'),
    ('thecrimson.com','news'),
    ('msnbc.msn.com','news'),
    ('salon.com','news'),
    ('motherjones.com','news'),
    ('kickstarter.com','donation'),
    ('owsnews.org','occupy'),
    ('blastmagazine.com','blog'),
    ('sacbee.com','news'),
    ('money.cnn.com','news'),
    ('kionrightnow.com','news'),
    ('foxnews.com','news'),
    ('occupywallstreetphotography.com','occupy'),
    ('thought.occupybucharest.com','occupy'),
    ('necn.com','news'),
    ('harvardcommunity.tumblr.com','blog'),
    ('thegatewaypundit.com','blog'),
    ('verumserum.com','blog'),
    ('rollingstone.com','news'),
    ('qik.com','stream'),
    ('plus.google.com','google'),
    ('aljazeera.com','news'),
]
