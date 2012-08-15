from itertools import chain
from django.views.generic.base import TemplateView

from structure.models import Issue
from stories.models import Story
from blog.models import Entry
from config.models import SiteConfig
from video.models import Video


class CurrentView(TemplateView):
    def get_context_data(self, **kwargs):
        context = {}
        context['sections'] = Issue.objects.latest().sections.get_sections()
        return context


class FrontView(CurrentView):
    '''
    Front Page
    '''
    template_name = 'front.html'

    def get_context_data(self, **kwargs):
        context = super(FrontView, self).get_context_data(**kwargs)

        latest_stories = Story.published.order_by('-pub_date')[:10]
        latest_entries = Entry.objects.filter(is_published=True) \
            .order_by('-pub_date')[:10]

        context['latest_stories'] = sorted(chain(latest_entries, latest_stories),
            key=lambda x: x.pub_date, reverse=True)[:5]

        latest_section = []
        for section in context['sections']:
            latest_section.extend(Story.published.filter(
                section=section, featured=True, \
                storyphoto__isnull=False).order_by('-pub_date')[:1])

        config = SiteConfig.get()
        if not config.featured_video:
            context['latest_video'] = Video.published.latest('pub_date')

        context['featured'] = config.featuredstory_set.all() \
            .order_by('story_order')
        context['latest_entries'] = latest_entries
        context['latest_section'] = latest_section
        return context
