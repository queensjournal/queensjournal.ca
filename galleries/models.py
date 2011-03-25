from django.db import models
from django.template.defaultfilters import slugify
from stories.models import Story, Photo

class Gallery(models.Model):
    name = models.CharField(max_length=255)
    story = models.ForeignKey(Story)
    images = models.ManyToManyField(Photo)

    class Meta:
        verbose_name = "Photo Gallery"
        verbose_name_plural = "Photo Galleries"

    def __unicode__(self):
        return self.name
