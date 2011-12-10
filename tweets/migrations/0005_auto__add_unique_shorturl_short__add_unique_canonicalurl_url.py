# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing index on 'ShortUrl', fields ['short']
        db.delete_index('tweets_shorturl', ['short'])

        # Adding unique constraint on 'ShortUrl', fields ['short']
        db.create_unique('tweets_shorturl', ['short'])

        # Removing index on 'CanonicalUrl', fields ['url']
        db.delete_index('tweets_canonicalurl', ['url'])

        # Adding unique constraint on 'CanonicalUrl', fields ['url']
        db.create_unique('tweets_canonicalurl', ['url'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'CanonicalUrl', fields ['url']
        db.delete_unique('tweets_canonicalurl', ['url'])

        # Adding index on 'CanonicalUrl', fields ['url']
        db.create_index('tweets_canonicalurl', ['url'])

        # Removing unique constraint on 'ShortUrl', fields ['short']
        db.delete_unique('tweets_shorturl', ['short'])

        # Adding index on 'ShortUrl', fields ['short']
        db.create_index('tweets_shorturl', ['short'])


    models = {
        'tweets.canonicalurl': {
            'Meta': {'object_name': 'CanonicalUrl'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        },
        'tweets.shorturl': {
            'Meta': {'object_name': 'ShortUrl'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'url': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tweets.CanonicalUrl']"})
        },
        'tweets.tweet': {
            'Meta': {'ordering': "['id']", 'object_name': 'Tweet'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'day': ('django.db.models.fields.DateField', [], {}),
            'from_user': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'from_user_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'geo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'hour': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'minute': ('django.db.models.fields.IntegerField', [], {}),
            'profile_image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'to_user': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'to_user_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'twitter_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'urls': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tweets.CanonicalUrl']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['tweets']
