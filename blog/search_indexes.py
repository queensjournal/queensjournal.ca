import datetime
from haystack.indexes import *
from haystack import site
from blog.models import Entry

class EntryIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	author = CharField(model_attr='author', faceted=True)
	pub_date = DateTimeField(model_attr='pub_date', faceted=True)
	tags = MultiValueField(model_attr='tags', faceted=True)
			
	def get_queryset(self):
		return Entry.objects.filter(pub_date__lte=datetime.datetime.now())
		
	def prepare_tags(self, obj):
		try:
			return [tag for tag in obj.tags]
		except TypeError:
			return False
		
site.register(Entry, EntryIndex)