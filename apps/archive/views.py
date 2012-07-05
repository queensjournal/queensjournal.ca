import datetime
from django.shortcuts import get_list_or_404, get_object_or_404, \
    render_to_response, redirect
from django.template import RequestContext

from structure.models import Volume, Issue, FrontPageConfig, FrontConfig, \
    SectionFrontConfig
from stories.models import Story
from stories.views import parse_date


def archive_index(request):
    volumes = get_list_or_404(Volume.objects.order_by('-volume'))
    dates = {}
    # TODO refactor this shit. Use an instance method instead
    for volume in volumes:
        try:
            first_issue = Issue.objects.filter(volume__volume=volume.volume).\
                order_by('pub_date')[0]
            last_issue = Issue.objects.filter(volume__volume=volume.volume).\
                order_by('-pub_date')[0]
            dates[volume.volume] = '%s - %s' % (first_issue.pub_date.
                strftime("%Y"), last_issue.pub_date.strftime("%Y"))
        except IndexError:
            continue
    return render_to_response('archives/index.html', {
                            'volumes': volumes,
                            'dates': dates
                            }, context_instance=RequestContext(request))


def archive_volume_index(request, volume):
    volume = get_object_or_404(Volume, volume=volume)
    issues = get_list_or_404(Issue, volume=volume,
        pub_date__lt=datetime.datetime.now())
    return render_to_response('archives/index_volume.html', {
                            'volume': volume,
                            'issues': issues,
                            }, context_instance=RequestContext(request))


def archive_issue_index(request, datestring):
    issue = get_object_or_404(Issue, pub_date=parse_date(datestring))
    sects = issue.sections.get_sections()
    sections = []
    for section in sects:
        sections.append({
            'name': section.name,
            'stories': Story.published.filter(section=section, issue=issue)
            })
    return render_to_response('archives/issue_detail.html', {
        'sections': sections,
        'issue': issue
        }, context_instance=RequestContext(request))


def section_index(request, datestring, section):
    # TODO: clean up this garbage
    issue = get_object_or_404(Issue, pub_date=parse_date(datestring))
    try:
        front_config = FrontPageConfig.objects.get(issue=issue)
    except FrontPageConfig.DoesNotExist:
        try:
            front_config = FrontConfig.objects.get(issue=issue)
        except FrontConfig.DoesNotExist:
            return redirect('stories.views.index_section', section=section)
    section_config = get_object_or_404(SectionFrontConfig.objects.filter(\
        section__slug__iexact=section))
    first_story = Story.objects.filter(section__slug__iexact=section, issue=issue, \
        status='p', storyphoto__isnull=False).order_by('section_order')
    story_set = Story.objects.filter(issue=issue, section__slug__iexact=section).\
        order_by('section_order')
    featured = []
    try:
        if first_story[0]:
            featured = first_story[0]
            other_stories = story_set[1:]
    except IndexError:
        other_stories = story_set
    try:
        last_story = other_stories.reverse()[0]
        older_stories = Story.objects.filter(section__slug__iexact=section, \
            pub_date__lt=last_story.pub_date).order_by('-pub_date')[:5]
    except IndexError:
        older_stories = Story.objects.filter(section__slug__iexact=section, \
            pub_date__lt=issue.pub_date).order_by('-pub_date')[:5]
    if request.session.get('vote') is None:
        request.session['vote'] = []
    return render_to_response('archives/index_section.html',
        {'featured': featured,
        'other_stories': other_stories,
        'older_stories': older_stories,
        'config': front_config,
        'section_config': section_config,
        'issue': issue},
        context_instance=RequestContext(request))
