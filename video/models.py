import datetime
from django.db import models
from imagekit.models import ImageModel
from structure.models import Author
from tagging.fields import TagField
from tagging.models import Tag

class Video(ImageModel):
	name = models.CharField(max_length=255)
	slug = models.SlugField(unique=True)
	pub_date = models.DateTimeField(default=datetime.datetime.now())
	link = models.URLField(help_text="Insert Link to YouTube or Vimeo video. e.g. http://www.youtube.com/watch?v=vnVkGSAqCIE. Make sure the link is http, not httpS")
	tags = TagField()
	caption = models.TextField()
	photographer = models.ForeignKey(Author, blank=True, null=True)
	screenshot = models.ImageField(upload_to='video_thumbs/%Y/%m/%d', help_text='Please convert all images to RGB JPEGs.')
	published = models.BooleanField()
	
	class IKOptions:
		# Defining ImageKit options
		spec_module = 'stories.video_specs'
		cache_dir = 'video_thumbs'
		image_field = 'screenshot'
		
	class Meta:
		ordering = ['-pub_date']
	
	@models.permalink	
	def get_absolute_url(self):
		return ('video.views.detail_video', (), {
			'datestring': self.pub_date.strftime("%Y-%m-%d"),
			'slug': self.slug})
			
	def __unicode__(self):
		return self.name
