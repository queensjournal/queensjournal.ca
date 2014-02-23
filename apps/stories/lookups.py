from selectable.base import ModelLookup
from selectable.registry import registry
from stories.models import Photo, Story


class PhotoLookup(ModelLookup):
    model = Photo
    search_fields = ('name__icontains', 'caption__icontains')

registry.register(PhotoLookup)


class StoryLookup(ModelLookup):
    model = Story
    search_fields = ('title__icontains', 'deck__icontains')

registry.register(StoryLookup)
