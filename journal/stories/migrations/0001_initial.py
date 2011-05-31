# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Story'
        db.create_table('stories_story', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('head', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('deck', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.Section'])),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.Issue'], null=True, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('summary', self.gf('django.db.models.fields.TextField')()),
            ('section_order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('enable_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('show_headshots', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 5, 31, 13, 27, 49, 938219), unique=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('is_tweeted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('stories', ['Story'])

        # Adding model 'StoryAuthor'
        db.create_table('stories_storyauthor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['structure.Author'])),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stories.Story'])),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('stories', ['StoryAuthor'])

        # Adding model 'Photo'
        db.create_table('stories_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.Issue'], null=True, blank=True)),
            ('caption', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('photographer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.Author'], null=True, blank=True)),
            ('credit', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2011, 5, 31))),
        ))
        db.send_create_signal('stories', ['Photo'])

        # Adding model 'StoryPhoto'
        db.create_table('stories_storyphoto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['stories.Photo'])),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stories.Story'])),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('stories', ['StoryPhoto'])

        # Adding model 'FeaturedPhoto'
        db.create_table('stories_featuredphoto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('original_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('stories', ['FeaturedPhoto'])

        # Adding model 'FeaturedStory'
        db.create_table('stories_featuredstory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stories.Story'])),
            ('front', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.FrontConfig'])),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stories.FeaturedPhoto'])),
            ('front_page', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('stories', ['FeaturedStory'])


    def backwards(self, orm):
        
        # Deleting model 'Story'
        db.delete_table('stories_story')

        # Deleting model 'StoryAuthor'
        db.delete_table('stories_storyauthor')

        # Deleting model 'Photo'
        db.delete_table('stories_photo')

        # Deleting model 'StoryPhoto'
        db.delete_table('stories_storyphoto')

        # Deleting model 'FeaturedPhoto'
        db.delete_table('stories_featuredphoto')

        # Deleting model 'FeaturedStory'
        db.delete_table('stories_featuredstory')


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
        'polls.poll': {
            'Meta': {'ordering': "('-pub_date', 'question')", 'object_name': 'Poll'},
            'close_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 6, 7, 13, 27, 49, 905174)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'question': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'stories.featuredphoto': {
            'Meta': {'object_name': 'FeaturedPhoto'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'original_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'stories.featuredstory': {
            'Meta': {'ordering': "['story__pub_date']", 'object_name': 'FeaturedStory'},
            'front': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structure.FrontConfig']"}),
            'front_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stories.FeaturedPhoto']"}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stories.Story']"})
        },
        'stories.photo': {
            'Meta': {'object_name': 'Photo'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2011, 5, 31)'}),
            'credit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structure.Issue']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'photographer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structure.Author']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'stories.story': {
            'Meta': {'ordering': "['-pub_date']", 'object_name': 'Story'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'deck': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'head': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_tweeted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structure.Issue']", 'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 5, 31, 13, 27, 49, 938219)', 'unique': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structure.Section']"}),
            'section_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'show_headshots': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'tags': ('tagging.fields.TagField', [], {})
        },
        'stories.storyauthor': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'StoryAuthor'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['structure.Author']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stories.Story']"})
        },
        'stories.storyphoto': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'StoryPhoto'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['stories.Photo']"}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stories.Story']"})
        },
        'structure.author': {
            'Meta': {'ordering': "['name']", 'object_name': 'Author'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'headshot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structure.Headshot']", 'null': 'True', 'blank': 'True'}),
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'structure.flatplanconfig': {
            'Meta': {'object_name': 'FlatPlanConfig'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'structure.frontconfig': {
            'Meta': {'ordering': "['-pub_date']", 'object_name': 'FrontConfig'},
            'announce_body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'announce_head': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structure.Issue']", 'null': 'True', 'blank': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Poll']", 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 5, 31, 13, 27, 49, 912987)'}),
            'sections': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structure.FlatPlanConfig']"})
        },
        'structure.headshot': {
            'Meta': {'object_name': 'Headshot'},
            'headshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'structure.issue': {
            'Meta': {'ordering': "['-pub_date']", 'object_name': 'Issue'},
            'extra': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.CharField', [], {'default': "'NPB'", 'max_length': '3'}),
            'issue': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'pub_date': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            'sections': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structure.FlatPlanConfig']"}),
            'volume': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structure.Volume']"})
        },
        'structure.section': {
            'Meta': {'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'structure.volume': {
            'Meta': {'object_name': 'Volume'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuu_embed': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['stories']
