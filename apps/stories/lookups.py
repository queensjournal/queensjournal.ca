from selectable.base import ModelLookup
from selectable.registry import registry
from stories.models import Photo


class PhotoLookup(ModelLookup):
    model = Photo
    search_fields = ('name__icontains', 'caption__icontains')

registry.register(PhotoLookup)
