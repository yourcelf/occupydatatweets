from django.db import models

class CanonicalUrl(models.Model):
    url = models.TextField(unique=True)

    def __unicode__(self):
        return unicode(self.url)

class ShortUrl(models.Model):
    short = models.URLField(unique=True)
    url = models.ForeignKey(CanonicalUrl)

    def __unicode__(self):
        return unicode(self.url)

class Tweet(models.Model):
    twitter_id = models.BigIntegerField()
    text = models.CharField(max_length=255)
    profile_image_url = models.URLField(blank=True)
    day = models.DateField()
    hour = models.IntegerField()
    minute = models.IntegerField()
    created_at = models.DateTimeField()
    geo = models.CharField(max_length=255, null=True)
    from_user = models.CharField(max_length=16)
    from_user_id = models.BigIntegerField()
    language = models.CharField(max_length=2)
    to_user = models.CharField(max_length=16, null=True)
    to_user_id = models.BigIntegerField(null=True)
    source = models.CharField(max_length=255)

    urls = models.ManyToManyField(CanonicalUrl)

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ['id']
