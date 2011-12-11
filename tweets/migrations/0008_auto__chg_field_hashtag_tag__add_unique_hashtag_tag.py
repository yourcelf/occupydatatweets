# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'HashTag.tag'
        db.alter_column('tweets_hashtag', 'tag', self.gf('django.db.models.fields.CharField')(unique=True, max_length=140))

        # Adding unique constraint on 'HashTag', fields ['tag']
        db.create_unique('tweets_hashtag', ['tag'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'HashTag', fields ['tag']
        db.delete_unique('tweets_hashtag', ['tag'])

        # Changing field 'HashTag.tag'
        db.alter_column('tweets_hashtag', 'tag', self.gf('django.db.models.fields.CharField')(max_length=255))


    models = {
        'tweets.canonicalurl': {
            'Meta': {'object_name': 'CanonicalUrl'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tweet_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        },
        'tweets.hashtag': {
            'Meta': {'object_name': 'HashTag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '140'})
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
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tweets.HashTag']", 'symmetrical': 'False'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'to_user': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'to_user_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'twitter_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'urls': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tweets.CanonicalUrl']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['tweets']
