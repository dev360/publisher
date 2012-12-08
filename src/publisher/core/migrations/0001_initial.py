# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profile'
        db.create_table('core_profile', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=40, primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='NEW', max_length=10)),
            ('activation_key', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('core', ['Profile'])

        # Adding model 'Feed'
        db.create_table('core_feed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='feeds', to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('price_plan', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('core', ['Feed'])

        # Adding unique constraint on 'Feed', fields ['publisher', 'slug']
        db.create_unique('core_feed', ['publisher_id', 'slug'])

        # Adding model 'FeedSubscriber'
        db.create_table('core_feedsubscriber', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Feed'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('core', ['FeedSubscriber'])

        # Adding model 'FeedReview'
        db.create_table('core_feedreview', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reviews', to=orm['core.Feed'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reviews', to=orm['auth.User'])),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('core', ['FeedReview'])

        # Adding model 'FeedItem'
        db.create_table('core_feeditem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(related_name='feed_items', to=orm['core.Feed'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('teaser', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_sample', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.CharField')(default='other', max_length=50, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('core', ['FeedItem'])

        # Adding unique constraint on 'FeedItem', fields ['feed', 'slug']
        db.create_unique('core_feeditem', ['feed_id', 'slug'])

        # Adding model 'Like'
        db.create_table('core_like', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='likes', to=orm['auth.User'])),
            ('feed_item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='likes', to=orm['core.FeedItem'])),
        ))
        db.send_create_signal('core', ['Like'])


    def backwards(self, orm):
        # Removing unique constraint on 'FeedItem', fields ['feed', 'slug']
        db.delete_unique('core_feeditem', ['feed_id', 'slug'])

        # Removing unique constraint on 'Feed', fields ['publisher', 'slug']
        db.delete_unique('core_feed', ['publisher_id', 'slug'])

        # Deleting model 'Profile'
        db.delete_table('core_profile')

        # Deleting model 'Feed'
        db.delete_table('core_feed')

        # Deleting model 'FeedSubscriber'
        db.delete_table('core_feedsubscriber')

        # Deleting model 'FeedReview'
        db.delete_table('core_feedreview')

        # Deleting model 'FeedItem'
        db.delete_table('core_feeditem')

        # Deleting model 'Like'
        db.delete_table('core_like')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.feed': {
            'Meta': {'unique_together': "(('publisher', 'slug'),)", 'object_name': 'Feed'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'price_plan': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feeds'", 'to': "orm['auth.User']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        'core.feeditem': {
            'Meta': {'unique_together': "(('feed', 'slug'),)", 'object_name': 'FeedItem'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feed_items'", 'to': "orm['core.Feed']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_sample': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'teaser': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'other'", 'max_length': '50', 'blank': 'True'})
        },
        'core.feedreview': {
            'Meta': {'object_name': 'FeedReview'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviews'", 'to': "orm['core.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviews'", 'to': "orm['auth.User']"})
        },
        'core.feedsubscriber': {
            'Meta': {'object_name': 'FeedSubscriber'},
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'core.like': {
            'Meta': {'object_name': 'Like'},
            'feed_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'likes'", 'to': "orm['core.FeedItem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'likes'", 'to': "orm['auth.User']"})
        },
        'core.profile': {
            'Meta': {'object_name': 'Profile'},
            'activation_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'NEW'", 'max_length': '10'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['core']