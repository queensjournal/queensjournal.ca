# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column('stories_story', 'head', 'title')

    def backwards(self, orm):
        db.rename_column('stories_story', 'title', 'head')
