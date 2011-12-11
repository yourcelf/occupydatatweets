from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^(?P<page>\d+)/(?P<sort>[-a-z_]+)/$', 'tweets.views.tweet_page', name='tweets.page'),
    url(r'^$', 'tweets.views.home', name='home'),
)

