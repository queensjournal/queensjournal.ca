# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'NewsCalendarItem'
        db.create_table(u'sidebars_newscalendaritem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('event_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sidebars.EventType'], null=True, blank=True)),
        ))
        db.send_create_signal(u'sidebars', ['NewsCalendarItem'])

        # Adding model 'ArtsCalendarItem'
        db.create_table(u'sidebars_artscalendaritem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('start_time', self.gf('django.db.models.fields.DateField')()),
            ('end_time', self.gf('django.db.models.fields.DateField')(default=None, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('event_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sidebars.EventType'])),
        ))
        db.send_create_signal(u'sidebars', ['ArtsCalendarItem'])

        # Adding model 'ArtsCalendarShowtime'
        db.create_table(u'sidebars_artscalendarshowtime', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sidebars.ArtsCalendarItem'])),
        ))
        db.send_create_signal(u'sidebars', ['ArtsCalendarShowtime'])

        # Adding model 'TalkingHeadsItem'
        db.create_table(u'sidebars_talkingheadsitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.Issue'], unique=True)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['polls.Poll'], null=True, blank=True)),
            ('photos_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.Author'], null=True)),
        ))
        db.send_create_signal(u'sidebars', ['TalkingHeadsItem'])

        # Adding model 'TalkingHeadsAnswer'
        db.create_table(u'sidebars_talkingheadsanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('quote', self.gf('django.db.models.fields.TextField')()),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stories.Photo'], null=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sidebars.TalkingHeadsItem'])),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'sidebars', ['TalkingHeadsAnswer'])

        # Adding model 'EventType'
        db.create_table(u'sidebars_eventtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'sidebars', ['EventType'])

        # Adding model 'SportsCalendarItem'
        db.create_table(u'sidebars_sportscalendaritem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sport', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sidebars.SportType'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ticket_info', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'sidebars', ['SportsCalendarItem'])

        # Adding model 'SportsTeamGameScore'
        db.create_table(u'sidebars_sportsteamgamescore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('home_team', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('home_score', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('away_team', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('away_score', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sidebars.SportsCalendarItem'])),
        ))
        db.send_create_signal(u'sidebars', ['SportsTeamGameScore'])

        # Adding model 'SportsIndividualScore'
        db.create_table(u'sidebars_sportsindividualscore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_detail', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('place', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('result_detail', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('home_team', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sidebars.SportsCalendarItem'])),
        ))
        db.send_create_signal(u'sidebars', ['SportsIndividualScore'])

        # Adding model 'SportType'
        db.create_table(u'sidebars_sporttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'sidebars', ['SportType'])


    def backwards(self, orm):
        
        # Deleting model 'NewsCalendarItem'
        db.delete_table(u'sidebars_newscalendaritem')

        # Deleting model 'ArtsCalendarItem'
        db.delete_table(u'sidebars_artscalendaritem')

        # Deleting model 'ArtsCalendarShowtime'
        db.delete_table(u'sidebars_artscalendarshowtime')

        # Deleting model 'TalkingHeadsItem'
        db.delete_table(u'sidebars_talkingheadsitem')

        # Deleting model 'TalkingHeadsAnswer'
        db.delete_table(u'sidebars_talkingheadsanswer')

        # Deleting model 'EventType'
        db.delete_table(u'sidebars_eventtype')

        # Deleting model 'SportsCalendarItem'
        db.delete_table(u'sidebars_sportscalendaritem')

        # Deleting model 'SportsTeamGameScore'
        db.delete_table(u'sidebars_sportsteamgamescore')

        # Deleting model 'SportsIndividualScore'
        db.delete_table(u'sidebars_sportsindividualscore')

        # Deleting model 'SportType'
        db.delete_table(u'sidebars_sporttype')


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 28, 14, 18, 35, 410295)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 28, 14, 18, 35, 409645)'}),
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
            'close_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 5, 14, 18, 35, 238760)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'question': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'sidebars.artscalendaritem': {
            'Meta': {'ordering': "('event_type', 'location', 'name', 'start_time')", 'object_name': 'ArtsCalendarItem'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sidebars.EventType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start_time': ('django.db.models.fields.DateField', [], {})
        },
        u'sidebars.artscalendarshowtime': {
            'Meta': {'ordering': "('time',)", 'object_name': 'ArtsCalendarShowtime'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sidebars.ArtsCalendarItem']"}),
            'time': ('django.db.models.fields.TimeField', [], {})
        },
        u'sidebars.eventtype': {
            'Meta': {'object_name': 'EventType'},
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'sidebars.newscalendaritem': {
            'Meta': {'ordering': "('start_time', 'end_time')", 'object_name': 'NewsCalendarItem'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sidebars.EventType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'sidebars.sportscalendaritem': {
            'Meta': {'ordering': "('start_time', 'sport')", 'object_name': 'SportsCalendarItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sport': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sidebars.SportType']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'ticket_info': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'sidebars.sportsindividualscore': {
            'Meta': {'ordering': "('event_detail', 'place')", 'object_name': 'SportsIndividualScore'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sidebars.SportsCalendarItem']"}),
            'event_detail': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'home_team': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'place': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'result_detail': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'sidebars.sportsteamgamescore': {
            'Meta': {'object_name': 'SportsTeamGameScore'},
            'away_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'away_team': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sidebars.SportsCalendarItem']"}),
            'home_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'home_team': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'sidebars.sporttype': {
            'Meta': {'object_name': 'SportType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'sidebars.talkingheadsanswer': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'TalkingHeadsAnswer'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stories.Photo']", 'null': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sidebars.TalkingHeadsItem']"}),
            'quote': ('django.db.models.fields.TextField', [], {})
        },
        u'sidebars.talkingheadsitem': {
            'Meta': {'ordering': "['issue']", 'object_name': 'TalkingHeadsItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['structure.Issue']", 'unique': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'photos_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['structure.Author']", 'null': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['polls.Poll']", 'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'stories.photo': {
            'Meta': {'object_name': 'Photo'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2013, 11, 28)'}),
            'credit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['structure.Issue']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'photographer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['structure.Author']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
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
        u'structure.flatplanconfig': {
            'Meta': {'object_name': 'FlatPlanConfig'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        u'structure.volume': {
            'Meta': {'object_name': 'Volume'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuu_embed': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['sidebars']
