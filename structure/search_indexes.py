import datetime
from haystack.indexes import *
from haystack import site
from structure.models import Author

class AuthorIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	bio = CharField(model_attr='bio', null=True)
	
site.register(Author, AuthorIndex)