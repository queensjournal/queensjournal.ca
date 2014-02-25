# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TextBox'
        db.create_table(u'bento_textbox', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('modification_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'bento', ['TextBox'])

        # Adding model 'ImageBox'
        db.create_table(u'bento_imagebox', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('modification_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('alternate_text', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'bento', ['ImageBox'])


    def backwards(self, orm):
        # Deleting model 'TextBox'
        db.delete_table(u'bento_textbox')

        # Deleting model 'ImageBox'
        db.delete_table(u'bento_imagebox')


    models = {
        u'bento.imagebox': {
            'Meta': {'object_name': 'ImageBox'},
            'alternate_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'bento.textbox': {
            'Meta': {'object_name': 'TextBox'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['bento']