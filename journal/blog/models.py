import re
from datetime import datetime
from django.db import models
from django.db.models import permalink
from structure.models import Author
from imagekit.models import ImageModel
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.query import QuerySet
from images.models import Image
from tagging.fields import TagField
from tagging.models import Tag
from dependencies.twitter_update import post_to_twitter

class BlogImage(ImageModel):
	slug = models.SlugField()
	image = models.ImageField(upload_to="blogs/", help_text="Bigger is better. Jpeg.")
	
	class IKOptions:
		# Defining ImageKit options
		spec_module = 'blog.blog_specs'
		cache_dir = 'photo_cache'
		image_field = 'image'
		
	class Meta:
		verbose_name = 'Blog Header Image'
		verbose_name_plural = 'Blog Header Images'
		
	def __unicode__(self):
		return self.slug

class Blog(models.Model):
	title = models.CharField(max_length=255, help_text='Short name for the blog.', unique=True)
	slug = models.SlugField(unique=True)
	description = models.TextField(blank=True, help_text="Description of the blog's content.")
	bloggers = models.ManyToManyField(Author)
	active = models.BooleanField('Blog is active?', default=True, help_text='You can disable blogs that are no longer being updated. They will be filed under the Archived Blogs page.')
	image = models.ForeignKey(BlogImage, blank=True, null=True)
	order = models.IntegerField(help_text="Order that the Blog will show up on the Blog page.")

	class Meta:
		ordering			= ('title',)

	def get_absolute_url(self):
		return('blog_index_front', (), {
			'blog': self.slug})
	get_absolute_url = permalink(get_absolute_url)

	def __unicode__(self):
		return self.title


class EntryManager(models.Manager):
	## single-blog/all blogs queryset functions
	def published(self):
		return self.get_query_set().filter(is_published=True).filter(pub_date__lte=datetime.now())

	def get_month(self, year, month):
		return self.published().filter(pub_date__year=year, pub_date__month=month)

	def get_by_author(self, author_id):
		return self.published().filter(author=author_id)

	## multiple-blog queryset functions
	def published_on_blog(self, blog):
		return self.published().filter(blog__slug__exact=blog)

	def get_month_on_blog(self, blog, year, month):
		return self.get_month(year, month).filter(blog__slug__exact=blog)

	def get_author_on_blog(self, blog, author_id):
		return self.get_by_author(author_id).filter(blog__slug__exact=blog)
		
	'''
	Sets up the ability to add custom methods to QuerySets
	
	def get_query_set(self):
		return self.model.QuerySet(self.model)
	def __getattr__(self, name, *args):
		if name.startswith('_'):
			raise AttributeError
		return getattr(self.get_query_set(), name, *args)
	'''
	
	def has_photos(self, blog):
		entries = self.published().filter(blog=blog).order_by('-pub_date')
		s_re = re.compile('<!--image:"([-\w]+)"-->',re.IGNORECASE)
		results = []
		for entry in entries:
			try:
				photo = Image.objects.get(slug__exact=s_re.findall(entry.content)[0])
				results.append(entry)
			except IndexError:
				continue
		return results

class Entry(models.Model):
	title = models.CharField(max_length=255, help_text='Title of the blog post.')
	blog = models.ForeignKey(Blog)
	slug = models.SlugField()
	author = models.ForeignKey(Author)
	tags = TagField(help_text='Post Tags and Label. Use this to apply tags to the post. Use commas to separate tags. The first tag will be the post\'s label. For example: \"Student Ghetto, EngSoc, Town-Gown, Aberdeen\"')
	content = models.TextField()
	is_published = models.BooleanField('Published', default=True, help_text='When you want to publish a blog post, make sure this box is checked; if you just want to save a draft, leave this unchecked.')
	enable_comments = models.BooleanField(default=True, help_text='Toggle to turn comments on or off for this post.')
	date_saved = models.DateTimeField(editable=False, default=datetime.now)
	date_draft_or_publish = models.DateTimeField(editable=False, default=datetime.now)
	pub_date = models.DateTimeField(default=datetime.now, blank=True, null=True, help_text='If you wish to keep a post hidden until some time in the future, check the Published box and change this date to when you want the post to go live.')
	is_tweeted = models.BooleanField(editable=False, default=False)
	objects = EntryManager()
	
	class Meta:
		ordering			= ('-date_draft_or_publish','-pub_date','-date_saved','title')
		verbose_name_plural = 'entries'
		permissions			= (('change_own_entry', 'Can change own entry'),
							   ('view_draft_entry', 'Can view all drafts and future posts'),
							   ('view_own_draft', 'Can view own drafts and future posts'),
							   ('delete_own_draft', 'Can delete own draft'),
							   ('moderate_entry', 'Can moderate comments on entries'))
		get_latest_by = '-pub_date'

	def save(self):
		# set pub_date time
		if self.is_published is True and self.pub_date is None:
			self.pub_date = datetime.now()
		elif self.is_published is False and self.pub_date is not None:
			self.pub_date = None
		# set date_draft_or_publish time
		if self.pub_date is None and self.date_draft_or_publish is None:
			self.date_draft_or_publish = datetime.now()
		elif self.pub_date is not None:
			self.date_draft_or_publish = self.pub_date
		# set slug
		if self.slug == 'slug-not-set' or self.slug is None:
			self.slug = slugify(self.title)[0:49]
		self.date_saved = datetime.now()
		super(Entry, self).save()
		
	def first_photo(self):
		s_re = re.compile('<!--image:"([-\w]+)"-->',re.IGNORECASE)
		try:
			photo = Image.objects.get(slug__exact=s_re.findall(self.content)[0])
			return photo
		except IndexError:
			return False

	def __unicode__(self):
		return '%s' % (self.title)

	def get_absolute_url(self):
		return('blog.views.blog_detail', (), {
			'blog': self.blog.slug,
			'year': self.pub_date.year,
			'month': self.pub_date.strftime('%m'),
			'slug': self.slug})
	get_absolute_url = permalink(get_absolute_url)
	
	def get_twitter_message(self):
		return u'%s: %s' % (self.title, self.content)

models.signals.post_save.connect(post_to_twitter, sender=Entry)
	

class Category(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(unique=True)
	banner = models.ImageField(upload_to='category/', blank=True, null=True, help_text='Small banner image to go along with the category, if applicable.')

	class Admin:
		list_display		= ('name',)

	class Meta:
		ordering			= ('name',)
		verbose_name_plural = 'categories'

	def __unicode__(self):
		return self.name

	def get_absolute_url(self):
		return('blog_archive_category_front', (), {
			'cat_slug': self.slug})
	get_absolute_url = permalink(get_absolute_url)
