from django.views.generic.base import TemplateView

from issues.models import Issue
from stories.models import Story
from blog.models import Entry
from config.models import SiteConfig
from video.models import Video


class CurrentView(TemplateView):
    pass


class FrontView(CurrentView):
    '''
    Front Page
    '''
    template_name = 'front.html'

    def get_context_data(self, **kwargs):
        context = super(FrontView, self).get_context_data(**kwargs)

        # TODO fuck all of this too
        latest_entries = Entry.objects.filter(is_published=True) \
            .order_by('-pub_date')[:10]

        context['latest_entries'] = latest_entries
        return context
