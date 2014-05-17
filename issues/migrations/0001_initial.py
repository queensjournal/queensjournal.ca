# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ('structure', '0002_auto__del_field_frontconfig_poll__del_field_frontpageconfig_poll'),
    )

    def forwards(self, orm):
        db.rename_table(u'structure_volume', u'issues_volume')
        db.rename_table(u'structure_issue', u'issues_issue')


    def backwards(self, orm):
        pass


    models = {
        u'issues.issue': {
            'Meta': {'ordering': "['-pub_date']", 'object_name': 'Issue'},
            'extra': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.CharField', [], {'default': "'NPB'", 'max_length': '3'}),
            'issue': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'pub_date': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            'sections': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['structure.FlatPlanConfig']"}),
            'volume': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['issues.Volume']"})
        },
        u'issues.volume': {
            'Meta': {'object_name': 'Volume'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuu_embed': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'})
        },
        u'structure.flatplanconfig': {
            'Meta': {'object_name': 'FlatPlanConfig'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['issues']
