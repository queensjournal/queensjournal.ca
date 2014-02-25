# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'StoryPoll'
        db.delete_table(u'inlines_storypoll')


    def backwards(self, orm):
        
        # Adding model 'StoryPoll'
        db.create_table(u'inlines_storypoll', (
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Poll'])),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stories.Story'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'inlines', ['StoryPoll'])


    models = {
        u'inlines.document': {
            'Meta': {'object_name': 'Document'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'files': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['inlines.DocumentFile']", 'symmetrical': 'False'}),
            'head': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stories.Story']"})
        },
        u'inlines.documentfile': {
            'Meta': {'object_name': 'DocumentFile'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'file_obj': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'inlines.factbox': {
            'Meta': {'object_name': 'Factbox'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'full_width': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'head': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stories.Story']"})
        },
        u'stories.story': {
            'Meta': {'ordering': "['-pub_date']", 'object_name': 'Story'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'deck': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'head': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_tweeted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['structure.Issue']", 'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'unique': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['structure.Section']"}),
            'section_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'show_headshots': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'d'", 'max_length': '1'}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'tags': ('tagging.fields.TagField', [], {})
        },
        u'structure.flatplanconfig': {
            'Meta': {'object_name': 'FlatPlanConfig'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'structure.issue': {
            'Meta': {'ordering': "['-pub_date']", 'object_name': 'Issue'},
            'extra': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.CharField', [], {'default': "'NPB'", 'max_length': '3'}),
            'issue': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'pub_date': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            'sections': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['structure.FlatPlanConfig']"}),
            'volume': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['structure.Volume']"})
        },
        u'structure.section': {
            'Meta': {'object_name': 'Section'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        u'structure.volume': {
            'Meta': {'object_name': 'Volume'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuu_embed': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['inlines']
