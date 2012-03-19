from django.db import models
from tagging.fields import TagField
from structure.models import Section
from video.models import Video
from stories.models import Story

class SiteConfig(models.Model):
    featured_tags = TagField()
    sections = models.ManyToManyField(Section)
    announcement_head = models.CharField(max_length=256, blank=True)
    announcement_body = models.TextField(blank=True)
    featured_video = models.ForeignKey(Video, blank=True, null=True, help_text="If this \
    isn't set the most recent video will be used.", default=None)

class FeaturedStory(models.Model):
    story = models.ForeignKey(Story)
    config = models.ForeignKey(SiteConfig)
    orig_photo = models.ImageField(upload_to='featured_photos/%Y/%m/%d')
    story_order = models.PositiveIntegerField(help_text="Lower the number, order it will \
        show in the Front slideshow")

    class IKOptions:
    # Defining ImageKit options
        spec_module = 'stories.featured_specs'
        cache_dir = 'photo_cache'
        image_field = 'orig_photo'

    class Meta:
        verbose_name = 'Top Story'
        verbose_name_plural = 'Top Story'
        ordering = ['story__pub_date']

    def __unicode__(self):
        from django.utils.encoding import force_unicode
        return 'Featured Story: %s' % (force_unicode(self.story.head))
