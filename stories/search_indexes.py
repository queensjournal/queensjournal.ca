import datetime
from haystack.indexes import SearchIndex, CharField, DateTimeField, MultiValueField
from haystack import site
from stories.models import Story, StoryAuthor
from tagging.models import Tag

class StoryIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    author = CharField(faceted=True)
    pub_date = DateTimeField(model_attr='pub_date', faceted=True)
    tags = MultiValueField(model_attr='tags', faceted=True)

    def get_queryset(self):
        return Story.objects.filter(pub_date__lte=datetime.datetime.now())

    def prepare_author(self, obj):
        try:
            sauthor = StoryAuthor.objects.filter(story__pub_date= \
                self.prepared_data['pub_date'])[0]
            author = sauthor.author
        except IndexError:
            author = u'Journal Staff'
        return author

    def prepare_tags(self, obj):
        tags = Tag.objects.get_for_object(Story.objects.filter(pub_date=\
            self.prepared_data['pub_date'])[0])
        if not tags is None:
            return tags
        else:
            return u'No Tags'

site.register(Story, StoryIndex)
