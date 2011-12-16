from django.db import models

class Domain(models.Model):
    domain = models.CharField(max_length=255, blank=True, unique=True)
    category = models.CharField(max_length=255, blank=True)
    subcategory = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u": ".join(self.domain, self.categories)

class CanonicalUrl(models.Model):
    url = models.TextField(unique=True)

    # denormalization
    domain = models.ForeignKey(Domain, null=True)
    first_appearance = models.DateTimeField(null=True)
    tweet_count = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.url)

class ShortUrl(models.Model):
    short = models.URLField(unique=True, db_index=True)
    url = models.ForeignKey(CanonicalUrl)

    def __unicode__(self):
        return unicode(self.url)

class HashTag(models.Model):
    tag = models.CharField(max_length=140, unique=True, db_index=True)

    def __unicode__(self):
        return unicode(self.tag)

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
    tags = models.ManyToManyField(HashTag)

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ['id']
