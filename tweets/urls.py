from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^pixel/(?P<sort>[-a-z_]+)/$', 'tweets.views.pixel_image', name='tweets.pixel_image'),
    url(r'^url/(?P<url_id>\d+)/$', 'tweets.views.url_detail', name='tweets.url_detail'),

    url(r'^(?P<page>\d+)/(?P<sort>[-a-z_]+)/$', 'tweets.views.tweet_page', name='tweets.page'),
    url(r'^$', 'tweets.views.home', name='home'),
)

