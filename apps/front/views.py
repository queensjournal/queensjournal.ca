import datetime
from itertools import chain
from operator import attrgetter
from django.views.generic.base import TemplateView
from structure.models import Issue, FrontPageConfig, FrontConfig, SectionFrontConfig
from stories.models import Story
from blog.models import Entry
from video.models import Video


class Front(TemplateView):
    '''
    Front Page
    '''
    template_name = 'front.html'

    def get_context_data(self, **kwargs):
        self.context = {}
        latest_stories = Story.objects.filter(status='p', \
            pub_date__lt=datetime.datetime.now()).order_by('-pub_date')[:5]
        latest_entries = Entry.objects.filter(is_published=True).order_by('-pub_date')[:5]
        latest_video = Video.objects.latest('pub_date')
        self.context['latest_stories'] = sorted(chain(latest_stories, latest_entries), \
            key=attrgetter('pub_date'))[:5]

        latest_section = []
        #for section in self.context['config'].sections.flatplansection_set.all():
            #latest_section.extend(Story.objects.filter(section=section.section,
                #featured=True, storyphoto__isnull=False, \
                #pub_date__lt=datetime.datetime.now()).order_by('-pub_date')[:1])

        #self.context['featured'] = self.context['config'].featuredstory_set.all().\
            #order_by('story_order')
        self.context['latest_entries'] = latest_entries
        self.context['latest_section'] = latest_section
        self.context['latest_video'] = latest_video
        return self.context
