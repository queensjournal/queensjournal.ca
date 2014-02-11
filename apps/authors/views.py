from django.views.generic.detail import DetailView
from utils.multiquery import MultiQuery

from .models import Author
from stories.models import StoryAuthor
from blog.models import Entry


class AuthorDetailView(DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        item = context['object']

        story_set = StoryAuthor.objects.filter(author__slug__exact=item,
            story__status='p').order_by('-story__pub_date')
        entry_set = Entry.objects.filter(author__slug__exact=item,
            is_published=True).order_by('-pub_date')
        context['items'] = MultiQuery(story_set, entry_set)

        return context
