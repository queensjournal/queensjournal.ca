# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Headshot'
        db.create_table(u'structure_headshot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('headshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'structure', ['Headshot'])

        # Adding model 'Author'
        db.create_table(u'structure_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('headshot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.Headshot'], null=True, blank=True)),
            ('homepage', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'structure', ['Author'])

        # Adding model 'AuthorRole'
        db.create_table(u'structure_authorrole', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.Author'])),
        ))
        db.send_create_signal(u'structure', ['AuthorRole'])

        # Adding model 'Volume'
        db.create_table(u'structure_volume', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('volume', self.gf('django.db.models.fields.PositiveSmallIntegerField')(unique=True)),
            ('issuu_embed', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'structure', ['Volume'])

        # Adding model 'Section'
        db.create_table(u'structure_section', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal(u'structure', ['Section'])

        # Adding model 'Issue'
        db.create_table(u'structure_issue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issue', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('volume', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.Volume'])),
            ('pub_date', self.gf('django.db.models.fields.DateField')(unique=True)),
            ('sections', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.FlatPlanConfig'])),
            ('extra', self.gf('django.db.models.fields.CharField')(max_length='255', null=True, blank=True)),
            ('is_published', self.gf('django.db.models.fields.CharField')(default='NPB', max_length=3)),
        ))
        db.send_create_signal(u'structure', ['Issue'])

        # Adding model 'FlatPlanConfig'
        db.create_table(u'structure_flatplanconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'structure', ['FlatPlanConfig'])

        # Adding model 'FlatPlanSection'
        db.create_table(u'structure_flatplansection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['structure.Section'])),
            ('config', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.FlatPlanConfig'])),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'structure', ['FlatPlanSection'])

        # Adding model 'SectionFrontConfig'
        db.create_table(u'structure_sectionfrontconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('announce_head', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('announce_body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.Section'], unique=True)),
        ))
        db.send_create_signal(u'structure', ['SectionFrontConfig'])

        # Adding model 'FrontConfig'
        db.create_table(u'structure_frontconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Poll'], null=True, blank=True)),
            ('announce_head', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('announce_body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 28, 14, 45, 3, 43913))),
            ('sections', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.FlatPlanConfig'])),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.Issue'], null=True, blank=True)),
        ))
        db.send_create_signal(u'structure', ['FrontConfig'])

        # Adding model 'FrontPageConfig'
        db.create_table(u'structure_frontpageconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.Issue'], unique=True)),
            ('announce_head', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('announce_body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Poll'], null=True, blank=True)),
        ))
        db.send_create_signal(u'structure', ['FrontPageConfig'])


    def backwards(self, orm):
        
        # Deleting model 'Headshot'
        db.delete_table(u'structure_headshot')

        # Deleting model 'Author'
        db.delete_table(u'structure_author')

        # Deleting model 'AuthorRole'
        db.delete_table(u'structure_authorrole')

        # Deleting model 'Volume'
        db.delete_table(u'structure_volume')

        # Deleting model 'Section'
        db.delete_table(u'structure_section')

        # Deleting model 'Issue'
        db.delete_table(u'structure_issue')

        # Deleting model 'FlatPlanConfig'
        db.delete_table(u'structure_flatplanconfig')

        # Deleting model 'FlatPlanSection'
        db.delete_table(u'structure_flatplansection')

        # Deleting model 'SectionFrontConfig'
        db.delete_table(u'structure_sectionfrontconfig')

        # Deleting model 'FrontConfig'
        db.delete_table(u'structure_frontconfig')

        # Deleting model 'FrontPageConfig'
        db.delete_table(u'structure_frontpageconfig')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 28, 14, 45, 3, 202030)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 28, 14, 45, 3, 201276)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'polls.poll': {
            'Meta': {'ordering': "('-pub_date', 'question')", 'object_name': 'Poll'},
            'close_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 5, 14, 45, 3, 36210)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'question': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'structure.author': {
            'Meta': {'ordering': "['name']", 'object_name': 'Author'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'headshot': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['structure.Headshot']", 'null': 'True', 'blank': 'True'}),
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'structure.authorrole': {
            'Meta': {'ordering': "['-start_date']", 'object_name': 'AuthorRole'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['structure.Author']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
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
            'section': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['structure.Section']"})
        },
        u'structure.frontconfig': {
            'Meta': {'ordering': "['-pub_date']", 'object_name': 'FrontConfig'},
            'announce_body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'announce_head': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['structure.Issue']", 'null': 'True', 'blank': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Poll']", 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 28, 14, 45, 3, 43913)'}),
            'sections': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['structure.FlatPlanConfig']"})
        },
        u'structure.frontpageconfig': {
            'Meta': {'object_name': 'FrontPageConfig'},
            'announce_body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'announce_head': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['structure.Issue']", 'unique': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Poll']", 'null': 'True', 'blank': 'True'})
        },
        u'structure.headshot': {
            'Meta': {'object_name': 'Headshot'},
            'headshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
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
        u'structure.sectionfrontconfig': {
            'Meta': {'ordering': "['section']", 'object_name': 'SectionFrontConfig'},
            'announce_body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'announce_head': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['structure.Section']", 'unique': 'True'})
        },
        u'structure.volume': {
            'Meta': {'object_name': 'Volume'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuu_embed': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['structure']
