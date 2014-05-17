from datetime import datetime
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.dates import MonthArchiveView
from blog.models import Blog, Entry
from tagging.models import Tag
from tagging.utils import calculate_cloud


class BlogListView(ListView):
    """
    List of all blogs.
    """

    model = Blog

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        context['latest'] = Entry.objects.filter(
            pub_date__lte=datetime.now()).order_by('-pub_date')[:5]
        return context


class BlogDetailView(ListView):

    model = Entry

    def get_queryset(self):
        self.blog = Blog.objects.get(slug=self.kwargs['slug'])
        return Entry.objects.filter(blog=self.blog)

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['blog'] = self.blog
        blog_tags = Tag.objects.usage_for_model(Entry, counts=True,
            filters=dict(blog__slug=self.kwargs['slug']))
        context['cloud'] = calculate_cloud(blog_tags)
        return context


class EntryMonthView(MonthArchiveView):
    """
    Monthly archives. Displays all blog posts in a given month. Paginated.
    """

    model = Entry
    date_field = 'pub_date'


class EntryDetail(DetailView):

    model = Entry
