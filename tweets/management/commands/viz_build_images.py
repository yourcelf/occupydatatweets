import os
import json
from collections import defaultdict

from django.core.management import BaseCommand
from django.conf import settings

from tweets.models import CanonicalUrl, Tweet
from tweets.vis import build_images

class Command(BaseCommand):
    args = ""
    help = "Generate images and data files for pixel-per-link visualizations"

    def handle(self, *args, **kwargs):
        sorts = (("-tweet_count", "count"), ("first_appearance", "date"))
        scales = (1, 2, 6)
        qs = CanonicalUrl.objects.exclude(
                domain__category="fail"
            ).exclude(
                first_appearance__isnull=True
            )
        #build_images(qs, sorts, scales)

        # Build category data
        cats = qs.values_list('domain__category', flat=True)
        cat_count = defaultdict(int)
        for cat in cats:
            cat_count[cat or "uncategorized"] += 1
        items = cat_count.items()
        items.sort(key=lambda a: a[1], reverse=True)
        extra_data = {
            'categories': items,
            'start_date': qs.order_by('first_appearance')[0].first_appearance.isoformat(),
            'end_date': Tweet.objects.order_by('-created_at')[0].created_at.isoformat(),
            'url_count': qs.count(),
            'tweet_count': Tweet.objects.exclude(urls__domain__category="fail").count(),
        }
        with open(os.path.join(settings.BASE, "static", "data", "pixel-categories.json"), 'w') as fh:
            json.dump(extra_data, fh)

