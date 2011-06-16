from django.db import models
import datetime
from django.template.defaultfilters import slugify
from stories.models import Story, Photo
from structure.models import Author

class PhotosPageOptions(models.Model):
    name = models.CharField(max_length=30, default="Photos Page Layout", editable=False)
    photographers = models.ManyToManyField(Author, help_text="Select which photographers to have their bios shown on the Photos page.")
    
    class Meta:
        verbose_name_plural = "Photos Page Options"
    
    def __unicode__(self):
        return self.name

class Gallery(models.Model):
    name = models.CharField(max_length=255)
    story = models.ForeignKey(Story)
    images = models.ManyToManyField(Photo, limit_choices_to = {'creation_date__gt': datetime.datetime.now() - datetime.timedelta(weeks=8)})

    class Meta:
        verbose_name = "Photo Gallery"
        verbose_name_plural = "Photo Galleries"

    def __unicode__(self):
        return self.name
