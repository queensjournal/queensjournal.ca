from django.db import models
import datetime
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
    slug = models.SlugField()
    story = models.ForeignKey(Story, null=True, blank=True)
    pub_date = models.DateField()
    description = models.TextField()
    images = models.ManyToManyField(Photo, limit_choices_to = {'creation_date__gt': datetime.datetime.now() - datetime.timedelta(weeks=8)})

    class Meta:
        verbose_name = "Photo Gallery"
        verbose_name_plural = "Photo Galleries"
        
    def first_photo(self):
        try:
            return self.images.all()[0]
        except:
            return False

    @models.permalink   
    def get_absolute_url(self):
        return ('galleries.views.gallery_detail', (), {
            'datestring': self.pub_date.strftime("%Y-%m-%d"),
            'slug': self.slug})

    def __unicode__(self):
        return self.name
