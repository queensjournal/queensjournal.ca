import datetime
from haystack.indexes import *
from haystack import site
from stories.models import Story, StoryAuthor

class StoryIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	author = StoryAuthor.objects.all()
	pub_date = DateTimeField(model_attr='pub_date')
	
	def get_queryset(self):
		return Story.objects.filter(pub_date__lte=datetime.datetime.now())
		
site.register(Story, StoryIndex)