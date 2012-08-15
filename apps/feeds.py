from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from structure.models import Section
from stories.models import Story
from blog.models import Blog, Entry
from video.models import Video
from itertools import chain
from django.template.defaultfilters import striptags


class LatestFeed(Feed):
    title = "Queen's Journal: Latest content"
    link = "/"
    description = "The latest from the Queen's Journal."
    title_template = "feeds/latest_title.html"
    description_template = 'feeds/latest_description.html'

    def items(self):
        results = chain(
                Story.published.select_related().order_by('-pub_date')[:10],
                Entry.objects.select_related().filter(is_published=True) \
                    .order_by('-pub_date')[:10],
                Video.objects.select_related().filter(is_published=True) \
                    .order_by('-pub_date')[:10]
            )
        return sorted(results, key=lambda x: x.pub_date, reverse=True)

    def item_author_name(self, obj):
        if obj.model_type() is 'Story':
            return obj.section
        elif obj.model_type() is 'Video':
            return 'Videos'
        elif obj.model_type() is 'Entry':
            return 'Journal Blogs - %s' % (obj.blog)

    def item_pubdate(self, obj):
        return obj.pub_date


class LatestStoriesFeed(Feed):
    title = "Queen's Journal: Latest stories"
    link = "/"
    description = "All the latest stories from the Queen's Journal."
    description_template = 'feeds/stories_description.html'

    def items(self):
        return Story.objects.select_related().filter(status='p').order_by('-pub_date')[:15]

    def item_author_name(self, item):
        return striptags(item.list_authors())

    def item_pubdate(self, item):
        return item.pub_date


class LatestStoriesSectionFeed(Feed):
    description_template = 'feeds/stories_description.html'

    def get_object(self, request, slug):
        """
        /rss/section/<slug>/: latest stories from <slug>
        """
        return get_object_or_404(Section, slug=slug)

    def title(self, obj):
        return "Queen's Journal: Latest stories in %s" % obj.name

    def link(self, obj):
        return "/%s/" % obj.slug

    def description(self, obj):
        return "The latest stories in %s from the Queen's Journal." % obj.name

    def items(self, obj):
        return Story.objects.select_related().filter(
            section__slug=obj.slug, status='p').order_by('-pub_date')[:15]

    def item_author_name(self, item):
        return striptags(item.list_authors())

    def item_pubdate(self, item):
        return item.pub_date


class LatestPostsAllBlogsFeed(Feed):
    title = "Queen's Journal: Latest posts from all blogs"
    link = "/blogs/"
    description = "All the latest blog posts from the Queen's Journal."

    def items(self):
        return Entry.objects.select_related().filter(is_published=True).order_by('-pub_date')[:15]

    def item_author_name(self, item):
        return item.blog

    def item_pubdate(self, item):
        return item.pub_date


class LatestPostsSingleBlogFeed(Feed):
    def get_object(self, request, slug):
        """
        /rss/blogs/<blog>/: latest posts from <blog>
        """
        return get_object_or_404(Blog, slug=slug)

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


class LatestVideosFeed(Feed):
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
