# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CanonicalUrl'
        db.create_table('tweets_canonicalurl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('tweets', ['CanonicalUrl'])

        # Adding model 'ShortUrl'
        db.create_table('tweets_shorturl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tweets.CanonicalUrl'])),
        ))
        db.send_create_signal('tweets', ['ShortUrl'])

        # Adding model 'Tweet'
        db.create_table('tweets_tweet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('twitter_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('profile_image_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('day', self.gf('django.db.models.fields.DateField')()),
            ('hour', self.gf('django.db.models.fields.IntegerField')()),
            ('minute', self.gf('django.db.models.fields.IntegerField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('geo', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('from_user', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('from_user_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('to_user', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
            ('to_user_id', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('tweets', ['Tweet'])


    def backwards(self, orm):
        
        # Deleting model 'CanonicalUrl'
        db.delete_table('tweets_canonicalurl')

        # Deleting model 'ShortUrl'
        db.delete_table('tweets_shorturl')

        # Deleting model 'Tweet'
        db.delete_table('tweets_tweet')


    models = {
        'tweets.canonicalurl': {
            'Meta': {'object_name': 'CanonicalUrl'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'tweets.shorturl': {
            'Meta': {'object_name': 'ShortUrl'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tweets.CanonicalUrl']"})
        },
        'tweets.tweet': {
            'Meta': {'object_name': 'Tweet'},
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
            'twitter_id': ('django.db.models.fields.BigIntegerField', [], {})
        }
    }

    complete_apps = ['tweets']
