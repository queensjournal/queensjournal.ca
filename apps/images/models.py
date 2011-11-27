from datetime import datetime
from django.db import models
from django.template.defaultfilters import slugify
from imagekit.models import ImageModel

class Image(ImageModel):
    name = models.CharField(max_length=255, unique=True, help_text='Descriptive name of \
        the image. Will be displayed as alt text.')
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='content/%Y/%m/')
    caption = models.TextField(blank=True, help_text='Caption for the image. Optional.')
    credit = models.CharField(max_length=64, blank=True, help_text='Image credit. Optional.')
    date_added = models.DateTimeField(default=datetime.now,editable=False)

    class IKOptions: # Defining ImageKit options
        spec_module = 'images.specs'
        cache_dir = 'photo_cache'
        image_field = 'image'

    def __unicode__(self):
        return self.name

    def save(self):
        if self.slug == '' or self.slug is None:
            self.slug = slugify(self.name)[0:49]
        super(Image, self).save()
