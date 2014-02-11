from django.views.generic.detail import DetailView

from .models import Section
from stories.models import Story
from issues.models import Issue


class SectionDetailView(DetailView):
    model = Section

    def get_context_data(self, **kwargs):
        context = super(SectionDetailView, self).get_context_data(**kwargs)
        section = context['object']
        # TODO refactor all this into templatetags
        context['featured'] = Story.objects.filter(section__slug__iexact=section,
            featured=True, status='p').exclude(storyphoto__isnull=True,
            gallery__isnull=True).order_by('-pub_date')[:5]

        story_set = Story.objects.filter(section__slug__iexact=section,
            status='p').order_by('-pub_date')
        context['latest_stories'] = story_set[:5]
        context['other_stories'] = story_set[5:13]
        context['latest_issue'] = Issue.objects.latest()
        return context

section_detail = SectionDetailView.as_view()
