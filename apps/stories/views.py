import datetime
from datetime import date, time, timedelta
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from stories.models import Story, StoryAuthor

# New
from structure.models import Issue, SectionFrontConfig


def parse_date(datestring):
    return date(*[int(x) for x in datestring.split('-')])


def index_section(request, section):
    section_config = get_object_or_404(SectionFrontConfig,
        section__slug__iexact=section)
    featured = Story.objects.filter(section__slug__iexact=section,
        featured=True, status='p').exclude(storyphoto__isnull=True,
            gallery__isnull=True).order_by('-pub_date')[:5]
    story_set = Story.objects.filter(section__slug__iexact=section,
        status='p').order_by('-pub_date')
    latest_stories = story_set[:5]
    other_stories = story_set[5:13]
    latest_issue = Issue.objects.latest()
    return render_to_response('stories/index_section.html',
        {'featured': featured,
        'latest_stories': latest_stories,
        'other_stories': other_stories,
        'config': section_config,
        'latest_issue': latest_issue, },
        context_instance=RequestContext(request))


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
    return render_to_response('stories/single_detail.html',
                                {'story': story_selected,
                                'author_role': author_role, },
                                context_instance=RequestContext(request))


def server_error(request, template_name='500.html'):
    # TODO move to utils or something
    return render_to_response(template_name, context_instance=RequestContext(request))
