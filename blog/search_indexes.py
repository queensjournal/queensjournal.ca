import datetime
from haystack.indexes import *
from haystack import site
from blog.models import Entry

class EntryIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	author = CharField(model_attr='author_id')
	pub_date = DateTimeField(model_attr='date_published')
	
	def get_queryset(self):
		return Entry.objects.filter(date_published__lte=datetime.datetime.now())
		
site.register(Entry, EntryIndex)