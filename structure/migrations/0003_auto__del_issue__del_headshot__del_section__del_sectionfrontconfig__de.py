# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ('authors', '0001_initial'),
        ('blog', '0001_initial'),
        ('issues', '0001_initial'),
        ('sections', '0001_initial'),
    )

    def forwards(self, orm):
        # Deleting model 'SectionFrontConfig'
        db.delete_table(u'structure_sectionfrontconfig')

        # Changing field 'FrontPageConfig.issue'
        db.alter_column(u'structure_frontpageconfig', 'issue_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issues.Issue'], unique=True))

        # Changing field 'FrontConfig.issue'
        db.alter_column(u'structure_frontconfig', 'issue_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issues.Issue'], null=True))

        # Changing field 'FlatPlanSection.section'
        db.alter_column(u'structure_flatplansection', 'section_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sections.Section']))

    def backwards(self, orm):
        db.rename_table(u'issues_volume', u'structure_volume')
        db.rename_table(u'issues_issue', u'structure_issue')

        db.rename_table(u'authors_headshot', u'structure_headshot')
        db.rename_table(u'authors_authorrole', u'structure_authorrole')
        db.rename_table(u'authors_author', u'structure_author')

        db.rename_table(u'sections_section', u'structure_section')

        # Adding model 'SectionFrontConfig'
        db.create_table(u'structure_sectionfrontconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.Section'], unique=True)),
            ('announce_body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('announce_head', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'structure', ['SectionFrontConfig'])

        # Changing field 'FrontPageConfig.issue'
        db.alter_column(u'structure_frontpageconfig', 'issue_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.Issue'], unique=True))

        # Changing field 'FrontConfig.issue'
        db.alter_column(u'structure_frontconfig', 'issue_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.Issue'], null=True))

        # Changing field 'FlatPlanSection.section'
        db.alter_column(u'structure_flatplansection', 'section_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.Section']))

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
        u'sections.section': {
            'Meta': {'object_name': 'Section'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'structure.flatplanconfig': {
            'Meta': {'object_name': 'FlatPlanConfig'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'structure.flatplansection': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'FlatPlanSection'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'config': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['structure.FlatPlanConfig']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['sections.Section']"})
        },
        u'structure.frontconfig': {
            'Meta': {'ordering': "['-pub_date']", 'object_name': 'FrontConfig'},
            'announce_body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'announce_head': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['issues.Issue']", 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 6, 0, 0)'}),
            'sections': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['structure.FlatPlanConfig']"})
        },
        u'structure.frontpageconfig': {
            'Meta': {'object_name': 'FrontPageConfig'},
            'announce_body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'announce_head': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['issues.Issue']", 'unique': 'True'})
        }
    }

    complete_apps = ['structure']
