import os
import math
import json
from collections import defaultdict
from django.conf import settings

from PIL import Image, ImageDraw

from tweets.models import CanonicalUrl

category_colors = {
    'fail': (0xaa, 0x99, 0x99),
    'donation': (0x99, 0xff, 0x99),
    'google': (0xff, 0xff, 0x99),
    'image': (255, 0x39, 0xae),
    'other': (0x99, 0x99, 0x99),
    'stream': (0x99, 0x33, 0xff),
    'tweet': (0x99, 0xaa, 0xff),
    'occupy': (0xff, 0xff, 0xff),
    'news': (0x7c, 0x6c, 0x47),
    'blog': (0x00, 0x88, 0x00),
    'wikipedia': (0xff, 0xd3, 0x48),
    'geo': (0x00, 0x33, 0x00),
    'fb': (0x11, 0x33, 0xaa),
    'video': (0xff, 0x00, 0x00),
    'uncategorized': (0x33, 0x33, 0x33),
}

def build_images(queryset, sorts, scales):
    categories = queryset.values_list('domain__category', flat=True).distinct()
    for sort, sort_name in sorts:
        surls = list(queryset.order_by(sort).select_related('domain'))
        urldata = [[
            url.url[0:35].replace("http://", "").replace("www.", "")[0:35], # limit for data size
            url.domain.category or "uncategorized",
            url.tweet_count,
            url.first_appearance.isoformat(),
            url.id,
        ] for url in surls]
        with open(os.path.join(settings.BASE, "static", "data",
                    "pixel-%s.json" % sort_name), 'w') as fh:
                json.dump(urldata, fh)

        for scale in scales:
            cols = int(math.floor(1000. / scale))
            rows = int(math.ceil(float(len(surls)) / cols))

            # Coords are coordinates of swatches, not pixels.
            coords = [(col, row) for col in xrange(cols) for row in xrange(rows)]
            coords.sort(key=lambda p: p[1])

            img = Image.new('RGB', [cols * scale, rows * scale])
            draw = ImageDraw.ImageDraw(img)
            mask_imgs = {}
            mask_draws = {}
            for cat in categories:
                mask_imgs[cat] = Image.new('RGBA', [cols * scale, rows * scale])
                mask_draws[cat] = ImageDraw.ImageDraw(mask_imgs[cat])

            for i, coord in enumerate(coords):
                try:
                    url = surls[i]
                except IndexError:
                    color = (0, 0, 0)
                else:
                    color = category_colors[url.domain.category or "other"]
                rect = (
                    (coord[0] * scale, coord[1] * scale), 
                    (coord[0] * scale + scale, coord[1] * scale + scale),
                )
                draw.rectangle(rect, color)
                for cat, mask in mask_draws.iteritems():
                    if cat == url.domain.category:
                        color = (color[0], color[1], color[2], 255)
                        mask.rectangle(rect, color)
                    else:
                        color = (color[0], color[1], color[2], 30)
                        mask.rectangle(rect, color)

            img.save(
                os.path.join(settings.BASE, "static", "img", 
                    "pixel-%s-%s.png" % (sort_name, scale))
            )
            for mask, im in mask_imgs.items():
                im.save(
                    os.path.join(settings.BASE, "static", "img",
                        "pixel-%s-%s-%s.png" % (sort_name, scale, mask or "uncategorized")
                    )
                )
                
