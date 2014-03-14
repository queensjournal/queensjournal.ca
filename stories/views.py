from datetime import date
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.detail import DetailView
from stories.models import Story


def parse_date(datestring):
    return date(*[int(x) for x in datestring.split('-')])


class StoryDetailView(DetailView):

    model = Story

    def get_queryset(self):
        return Story.objects.published()

story_detail = StoryDetailView.as_view()


def server_error(request, template_name='500.html'):
    # TODO move to utils or something
    return render_to_response(template_name, context_instance=RequestContext(request))
