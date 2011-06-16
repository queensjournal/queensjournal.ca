from datetime import datetime, timedelta
from django.contrib.syndication.feeds import Feed
from structure.models import Issue, Section, FlatPlanConfig
from stories.models import Story
from sidebars.models import NewsCalendarItem, ArtsCalendarItem, SportsCalendarItem
from blog.models import Blog, Entry
from video.models import Video
from itertools import chain
from operator import attrgetter

class Latest(Feed):
    title = "Queen's Journal: Latest content"
    link = "/"
    description = "The latest from the Queen's Journal."
    title_template = "feeds/latest_title.html"
    description_template = 'feeds/latest_description.html'
    
    def items(self):
        stories = Story.objects.select_related().filter(status='p').order_by('-pub_date')[:10]
        entries = Entry.objects.select_related().filter(is_published=True).order_by('-pub_date')[:10]
        videos = Video.objects.select_related().filter(is_published=True).order_by('-pub_date')[:10]
        return sorted(chain(stories, entries, videos), key=attrgetter('pub_date'))[:30]
        
    def item_author_name(self, obj):
        if obj.model_type() is 'Story':
            return obj.section
        elif obj.model_type() is 'Video':
            return 'Videos'
        elif obj.model_type() is 'Entry':
            return 'Journal Blogs - %s' % (obj.blog)
            
    def item_pubdate(self, obj):
        return obj.pub_date

class LatestStories(Feed):
	title = "Queen's Journal: Latest stories"
	link = "/"
	description = "All the latest stories from the Queen's Journal."
	description_template = 'feeds/stories_description.html'

	def items(self):
		return Story.objects.select_related().filter(status='p').order_by('-pub_date')[:15]

	def item_author_name(self, item):
		return item.section

	def item_pubdate(self, item):
		return item.pub_date

class LatestStoriesSection(Feed):
	description_template = 'feeds/stories_description.html'
	def get_object(self, bits):
		"""
		/rss/section/<section>/: latest stories from <section>
		"""
		if len(bits) != 1:
			raise ObjectDoesNotExist
		else:
			return Section.objects.get(slug__exact=bits[0])
		
	def title(self, obj):
		return "Queen's Journal: Latest stories in %s" % obj.name

	def link(self, obj):
		return "/%s/" % obj.slug

	def description(self, obj):
		return "The latest stories in %s from the Queen's Journal." % obj.name

	def items(self, obj):
		return Story.objects.select_related().filter(section__slug=obj.slug, status='p').order_by('-pub_date')[:15]

	def item_author_name(self, item):
		return item.list_authors()

	def item_pubdate(self, item):
		return item.pub_date


class LatestPostsAllBlogs(Feed):
	title = "Queen's Journal: Latest posts from all blogs"
	link = "/blogs/"
	description = "All the latest blog posts from the Queen's Journal."

	def items(self):
		return Entry.objects.select_related().filter(is_published=True).order_by('-pub_date')[:15]

	def item_author_name(self, item):
		return item.blog

	def item_pubdate(self, item):
		return item.pub_date


class LatestPostsSingleBlog(Feed):
	def get_object(self, bits):
		"""
		/rss/blogs/<blog>/: latest posts from <blog>
		"""
		if len(bits) != 1:
			raise ObjectDoesNotExist
		else:
			return Blog.objects.get(slug__exact=bits[0])
		
	def title(self, obj):
		return "Queen's Journal: Latest blog posts in %s" % obj.title

	def link(self, obj):
		return obj.get_absolute_url()

	def description(self, obj):
		return "The latest blog posts in %s from the Queen's Journal." % obj.title

	def items(self, obj):
		return Entry.objects.select_related().filter(blog__slug=obj.slug, is_published=True).order_by('-pub_date')[:15]

	def item_author_name(self, item):
		return item.blog

	def item_pubdate(self, item):
		return item.pub_date


class LatestPostsSingleAuthor(Feed):
	def get_object(self, bits):
		"""
		/rss/blog-author/<author-id>/: latest posts from <author-id>
		"""
		if len(bits) != 1:
			raise ObjectDoesNotExist
		else:
			return AuthorProfile.objects.get(pk=bits[0])
		
	def title(self, obj):
		return "Queen's Journal: Latest blog posts from %s" % obj.user.get_full_name()

	def link(self, obj):
		return obj.get_absolute_url()

	def description(self, obj):
		return "The latest blog posts by %s from the Queen's Journal." % obj.user.get_full_name()

	def items(self, obj):
		return Entry.objects.select_related().filter(author=obj, is_published=True).order_by('-pub_date')[:15]

	def item_author_name(self, item):
		return item.blog

	def item_pubdate(self, item):
		return item.pub_date
		
class LatestVideos(Feed):
	title = "Queen's Journal: Latest videos"
	link = "/"
	description = "All the latest videos from the Queen's Journal."
	description_template = 'feeds/video_description.html'

	def items(self):
		return Video.objects.select_related().filter(is_published=True).order_by('-pub_date')[:15]

	def item_author_name(self, item):
		return item.photographer

	def item_pubdate(self, item):
		return item.pub_date  

