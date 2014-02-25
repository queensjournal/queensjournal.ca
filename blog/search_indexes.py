import datetime
from haystack.indexes import SearchIndex, CharField, DateTimeField, MultiValueField
from haystack import site
from blog.models import Entry
from tagging.models import Tag

class EntryIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    author = CharField(model_attr='author', faceted=True)
    pub_date = DateTimeField(model_attr='pub_date', faceted=True)
    tags = MultiValueField(model_attr='tags', faceted=True)

    def get_queryset(self):
        return Entry.objects.filter(pub_date__lte=datetime.datetime.now())

    def prepare_tags(self, obj):
        tags = Tag.objects.get_for_object(Entry.objects.filter(
            pub_date = self.prepared_data['pub_date'])[0])
        if not tags is None:
            return tags
        else:
            return u'No Tags'

site.register(Entry, EntryIndex)
