import datetime
import time
from django.db import models
from structure.models import *
from imagekit.models import ImageModel

class Story(models.Model):
	head = models.CharField(max_length=255)
	kick = models.CharField(max_length=255)
	slug = models.SlugField(help_text='Automatically generated')
	pub_date = models.DateTimeField('date published')
	section = models.ForeignKey(Section)
	issue = models.ForeignKey(Issue, blank=True, null=True, help_text="Enter an Issue if the story appeared in print. Otherwise it will be posted as a free-floating web story.")
	label = models.CharField(max_length=255, blank=True, help_text='ex. Signed Editorial, Feature. Optional.')
	content = models.TextField()
	summary = models.TextField(help_text="Sum up the story in a sentence or two. More for stories featured up top on the front page.")
	published = models.BooleanField(default=True)
	front = models.BooleanField(default=False, help_text="Check this to have the story automatically pushed to the front page. Testing.")
	twitter = models.BooleanField(default=True, help_text="Check this to get the story automatically put in the Tweet queue.")

	class Meta:
		verbose_name_plural = "Stories"
	
	def __unicode__(self):
		return self.head
	
	@models.permalink	
	def get_absolute_url(self):
		return ('journal.stories.views.detail_story', (), {
			'datestring': self.pub_date.strftime("%Y-%m-%d"),
			'section': self.section.slug,
			'slug': self.slug})
		
class Photo(ImageModel):
	name = models.CharField(max_length=50)
	slug = models.SlugField(max_length=50, unique=True)
	
	### ImageKit stuff
	original_image = models.ImageField(upload_to='photos')
	num_views = models.PositiveIntegerField(editable=False, default=0)
	
	class IKOptions:
		# Defining ImageKit options
		spec_module = 'stories.specs'
		cache_dir = 'photo_cache'
		image_field = 'original_image'
		save_count_as = 'num_views'
		
class FeaturedPhoto(ImageModel):
	name = models.CharField(max_length=50)
	slug = models.SlugField(max_length=50, unique=True)
	
	### ImageKit stuff
	original_image = models.ImageField(upload_to='featured_photos')
	num_views = models.PositiveIntegerField(editable=False, default=0)
	
	class IKOptions:
		# Defining ImageKit options
		spec_module = 'stories.featured_specs'
		cache_dir = 'photo_cache'
		image_field = 'original_image'
		save_count_as = 'num_views'
		
class StoryPhoto(models.Model):
	photo = models.ForeignKey(Photo, default=None)
	story = models.ForeignKey(Story)
		
class FeaturedStory(models.Model):
	from journal.structure.models import FrontPageConfig
	story = models.ForeignKey(Story, default=None)
	photo = models.ForeignKey(FeaturedPhoto, verbose_name='Photo for story. 700px x 300px.')
	headline = models.CharField('Headline', max_length=50, blank=True, null=True)
	front_page = models.ForeignKey(FrontPageConfig)
	
	class Meta:
		verbose_name = 'Top Story'
		verbose_name_plural = 'Top Story'
		
class FrontPageTopTierStory(models.Model):
	from journal.structure.models import FrontPageConfig
	story = models.ForeignKey(Story, default=None)
	headline = models.CharField('Optional frontpage headline', max_length=160, blank=True)
	front_page = models.ForeignKey(FrontPageConfig)
	
	class Meta:
		verbose_name = 'Top Tier Story (headline only)'
		verbose_name_plural = 'Top Tier Story (headline only)'
		order_with_respect_to = 'front_page'