from datetime import datetime
import time
from django.db import models
from structure.models import Issue, Section, FrontConfig, SectionFrontConfig, FrontPageConfig, Author
from imagekit.models import ImageModel
from tagging.fields import TagField
from tagging.models import Tag

STATUS_CHOICES = (
	('d', 'Draft'),
	('p', 'Published'),
	('w', 'Withdrawn'),
)

class Story(models.Model):
	head = models.CharField(max_length=255)
	kick = models.CharField(max_length=255, blank=True, null=True)
	slug = models.SlugField(help_text='Automatically written based on the headline. If nothing shows up here, try typing in the headline instead of copying and pasting. If a story with the same slug already exists for the given issue and section, just change the slug slightly so it doesn\'t conflict.')
	section = models.ForeignKey(Section)
	issue = models.ForeignKey(Issue, null=True, blank=True)
	label = models.CharField(max_length=255, blank=True, help_text='ex. "Signed Editorial," "Feature." Optional.')
	content = models.TextField()
	summary = models.TextField(help_text='Sum up the story in a single paragraph.')
	section_order = models.PositiveSmallIntegerField("Order in section", help_text="Determines the order of all stories in the section, with lower numbers at the top (so a story with order priority 1 would be at the top).")
	enable_comments = models.BooleanField(default=True)
	featured = models.BooleanField()
	tags = TagField(blank=True, null=True)
	pub_date = models.DateTimeField(default=datetime.now())
	status = models.CharField(max_length=1, choices=STATUS_CHOICES)

	class Meta:
		verbose_name_plural = "Stories"
		
	def list_authors(self):
		authors = []
		author_qset = list(self.storyauthor_set.all())
		author_num = len(author_qset)
		# byline names
		for wrapper in author_qset:
			if (author_num > 1 and wrapper != author_qset[-2]) or author_num == 1:
				authors.append(wrapper.author.name + ',')
			else:
				authors.append(wrapper.author.name)
		# byline titles
		if author_num > 1:
			authors.insert(-1, 'and')
			authors.append('Journal Staff')
		elif author_num == 1:
			authors.append(author_qset[0].author.get_role(self.pub_date))
		elif author_num == 0:
			authors.append('[no author]')
		return ' '.join(authors)
	list_authors.short_description = 'Author(s)'
		
	def set_tags(self, tags):
		Tag.objects.update_tags(self, tags)

	def get_tags(self, tags):
		return Tag.objects.get_for_object(self)
	
	def __unicode__(self):
		return self.head
		
	def get_absolute_url(self):
		return ('stories.views.detail_story', (), {
			'datestring': self.pub_date.strftime("%Y-%m-%d"),
			'section': self.section.slug,
			'slug': self.slug})
	get_absolute_url = models.permalink(get_absolute_url)
	
class StoryAuthor(models.Model):
	author = models.ForeignKey(Author, default=None)
	story = models.ForeignKey(Story)

	class Meta:
		order_with_respect_to = 'story'
		
class Photo(ImageModel):
	name = models.CharField(max_length=255, unique=True)
	slug = models.SlugField(unique=True, help_text='Automatically written based on the headline. If nothing shows up here, try typing in the headline instead of copying and pasting.')
	photo = models.ImageField(upload_to='stories/', help_text='The following sizes are used on the Journal site: 390 pixels high x 234 pixels wide (front page, top story); 390 pixels wide, any height (other stories); 100 pixels wide x 90 pixels tall (talking heads). Please convert all images to RGB JPEGs.')
	thumbnail = models.ImageField(upload_to='thumbs/', editable=False)
	issue = models.ForeignKey(Issue)
	caption = models.TextField(blank=True)
	photographer = models.ForeignKey(Author, blank=True, null=True)
	credit = models.CharField("Optional credit", max_length=255, help_text="For special photo credits not involving a staff photographer, ex. 'Photo courtesy of Queen's Alumni Services,' 'Journal File Photo,' etc.", blank=True)
	creation_date = models.DateField(default=datetime.now())
	
	### ImageKit stuff
	#original_image = models.ImageField(upload_to='photos')
	#num_views = models.PositiveIntegerField(editable=False, default=0)
	'''
	class IKOptions:
		# Defining ImageKit options
		spec_module = 'stories.specs'
		cache_dir = 'photo_cache'
		image_field = 'original_image'
		save_count_as = 'num_views'
	''' 
	def list_photographer(self):
		if self.photographer is not None:
			return self.photographer
		elif self.credit != '':
			return self.credit
		else:
			return '[no credit]'
	list_photographer.short_description = 'Credit'
	
	def get_absolute_url(self):
		return self.photo
	get_absolute_url = models.permalink(get_absolute_url)
	
	def __unicode__(self):
		return self.name
		
class FeaturedPhoto(ImageModel):
	name = models.CharField(max_length=50)
	slug = models.SlugField(max_length=50, unique=True)
	
	### ImageKit stuff
	original_image = models.ImageField(upload_to='featured_photos')
	
	class IKOptions:
		# Defining ImageKit options
		spec_module = 'stories.featured_specs'
		cache_dir = 'photo_cache'
		image_field = 'original_image'
		
	def __unicode__(self):
		return self.name
		
class StoryPhoto(models.Model):
	photo = models.ForeignKey(Photo, default=None)
	story = models.ForeignKey(Story)
	
	class Meta:
		verbose_name = "Story photos (click Save and Continue Editing to add more photo slots)"
		verbose_name_plural = "Story photos (click Save and Continue Editing to add more photo slots)"
		order_with_respect_to = 'story'
		
class FeaturedStory(models.Model):
	story = models.ForeignKey(Story, default=None)
	photo = models.ForeignKey(FeaturedPhoto, verbose_name='Photo for story. 700px x 300px.')
	front_page = models.ForeignKey(FrontConfig)
	
	class Meta:
		verbose_name = 'Top Story'
		verbose_name_plural = 'Top Story'
		
	def __unicode__(self):
		return 'Featured Story: %s' % (self.story,)
		
class FrontPageTopTierStory(models.Model):
	from structure.models import FrontPageConfig
	story = models.ForeignKey(Story, default=None)
	headline = models.CharField('Optional frontpage headline', max_length=160, blank=True)
	front_page = models.ForeignKey(FrontPageConfig)
	
	class Meta:
		verbose_name = 'Top Tier Story (headline only)'
		verbose_name_plural = 'Top Tier Story (headline only)'
		order_with_respect_to = 'front_page'

class FrontPageTopStory(models.Model):
	story = models.ForeignKey(Story, default=None)
	photo = models.ForeignKey(Photo, verbose_name='stand-alone photo (if top story has no photo)', blank=True, null=True)
	photohead = models.CharField('Photo headline', max_length=255, blank=True, null=True)
	front_page = models.ForeignKey(FrontPageConfig)

	class Meta:
		verbose_name = 'Top Story'
		verbose_name_plural = 'Top Story'
		
class FrontPageFirstTierStory(models.Model):
	story = models.ForeignKey(Story, default=None)
	label = models.CharField('Optional story label', max_length=255, blank=True, null=True)
	front_page = models.ForeignKey(FrontPageConfig)

	class Meta:
		verbose_name = 'First Tier Story (full summary)'
		verbose_name_plural = 'First Tier Stories (full summary)'
		order_with_respect_to = 'front_page'
		
class FrontPageSecondTierStory(models.Model):
	story = models.ForeignKey(Story, default=None)
	front_page = models.ForeignKey(FrontPageConfig)

	class Meta:
		verbose_name = 'Second Tier Story (headline only)'
		verbose_name_plural = 'Second Tier Stories (headline only)'
		order_with_respect_to = 'front_page'