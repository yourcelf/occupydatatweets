import json
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from tweets.models import CanonicalUrl

def _get_data(request, page, sort, per_page):
    try:
        page = int(page)
    except ValueError:
        raise Http404
    orders = {
        'count': "-tweet_count", 
        'date': "first_appearance"
    }
    if sort not in orders:
        sort = orders['count']
    urls = CanonicalUrl.objects.select_related('domain').exclude(
            domain__category=''
    ).order_by(orders[sort])

    p = Paginator(urls, per_page=per_page)
    try:
        results = p.page(page)
    except (InvalidPage, EmptyPage):
        raise Http404()

    out = []
    for url in results.object_list:
        out.append({
            'url': url.url,
            'tweet_count': url.tweet_count,
            'category': url.domain.category,
            'subcategory': url.domain.subcategory,
            'first_appearance': url.first_appearance.strftime("%Y %b %d"),
        })
    data = {
        'results': out,
        'page': page,
        'pages': p.num_pages,
        'next_link': reverse('tweets.page', kwargs={'page': page + 1, 'sort': sort}) if page < p.num_pages else '',
        'prev_link': reverse('tweets.page', kwargs={'page': page - 1, 'sort': sort}) if page > 1 else '',
        'order_links': [
            (reverse('tweets.page', kwargs={'page': page, 'sort': o}), orders[o].strip('-').replace('_', ' ')) for o in orders
        ],
    }
    return data

def tweet_page(request, page=1, sort='count'):
    return render(request, "tweets/tweets.html", {
        'data': json.dumps(_get_data(request, page, sort, 1000))
    })

def home(request):
    return redirect("tweets.page", page=1, sort='date')
