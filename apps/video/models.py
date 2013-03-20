import datetime
from django.db import models
from imagekit.models import ImageModel
from structure.models import Author
from video.managers import PublishedVideoManager
from tagging.fields import TagField


class Video(ImageModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now,
        auto_now_add=True)
    link = models.URLField(
        help_text="Insert Link to YouTube or Vimeo video. e.g. \
            http://www.youtube.com/watch?v=vnVkGSAqCIE. Make sure the link is \
            http, not httpS")
    tags = TagField()
    caption = models.TextField()
    photographer = models.ForeignKey(Author, blank=True, null=True)
    screenshot = models.ImageField(upload_to='video_thumbs/%Y/%m/%d',
        help_text='Please convert all images to RGB JPEGs.')
    is_published = models.BooleanField()
    is_tweeted = models.BooleanField(editable=False, default=False)

    objects = models.Manager()
    published = PublishedVideoManager()

    class IKOptions:
        # Defining ImageKit options
        spec_module = 'video.specs'
        cache_dir = 'photo_cache'
        image_field = 'screenshot'

    class Meta:
        ordering = ['-pub_date']

    @models.permalink
    def get_absolute_url(self):
        return ('video.views.video_detail', (), {
            'datestring': self.pub_date.strftime("%Y-%m-%d"),
            'slug': self.slug})

    def get_twitter_message(self):
        return u'Video: %s: %s' % (self.name)

    def model_type(self):
        return self.__class__.__name__

    def __unicode__(self):
        return self.name
