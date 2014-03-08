import datetime
from datetime import date, time, timedelta
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from stories.models import Story, StoryAuthor

from issues.models import Issue


def parse_date(datestring):
    return date(*[int(x) for x in datestring.split('-')])


def detail_story(request, datestring, section, slug):
    ## Set up a range of one day based on the datestring
    dt = datetime.datetime.combine(parse_date(datestring), time())
    dt2 = dt + timedelta(1) - datetime.datetime.resolution
    story_selected = get_object_or_404(Story, section__slug__exact=section,
        pub_date__range=(dt, dt2), slug__exact=slug, status='p')
    try:
        author = StoryAuthor.objects.filter(story__slug__exact=slug)[0]
        author_role = author.author.get_role(story_selected.pub_date)
    except IndexError:
        author_role = False
    return render_to_response('stories/story_detail.html',
                                {'story': story_selected,
                                'author_role': author_role, },
                                context_instance=RequestContext(request))


def server_error(request, template_name='500.html'):
    # TODO move to utils or something
    return render_to_response(template_name, context_instance=RequestContext(request))
