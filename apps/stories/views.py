import datetime
from django.conf import settings
from datetime import date, time, timedelta
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext, Context, loader
from django.http import HttpResponseRedirect
from stories.models import Story, StoryAuthor
from django.contrib.sites.models import Site
from stories.forms import EmailStoryForm
from django.core.mail import send_mail

# New
from structure.models import Issue, FrontPageConfig, FrontConfig, SectionFrontConfig


def parse_date(datestring):
    return date(*[int(x) for x in datestring.split('-')])


def get_issue(request):
    issue = get_object_or_404(Issue, pk=request.GET.get('issue', ''))
    return HttpResponseRedirect('/story/%s/' % issue.pub_date)


def index_section(request, section):
    section_config = get_object_or_404(SectionFrontConfig, section__slug__iexact=section)
    featured = Story.objects.filter(section__slug__iexact=section, featured=True, \
        status='p').exclude(storyphoto__isnull=True, gallery__isnull=True).\
        order_by('-pub_date')[:5]
    story_set = Story.objects.filter(section__slug__iexact=section, status='p').\
        order_by('-pub_date')
    latest_stories = story_set[:5]
    other_stories = story_set[5:13]
    latest_issue = Issue.objects.latest()
    # TODO: move all this vote stuff somewhere. Do we even need polls anymore?
    if request.session.get('vote') is None:
        request.session['vote'] = []
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
    story_selected = get_object_or_404(Story, section__slug__exact=section, \
        pub_date__range=(dt, dt2), slug__exact=slug, status='p')
    try:
        author = StoryAuthor.objects.filter(story__slug__exact=slug)[0]
        author_role = author.author.get_role(story_selected.pub_date)
    except IndexError:
        author_role = False
    if request.session.get('vote') is None:
        request.session['vote'] = []
    return render_to_response('stories/single_detail.html',
                                {'story': story_selected,
                                'author_role': author_role, },
                                context_instance=RequestContext(request))

''' ------------  STORIES -------------- '''


#TODO refactor, review, test. Move to external service?
def email_story(request, datestring, section, slug):
    if request.method != "POST":
        form = EmailStoryForm()
        article = get_object_or_404(Story, issue__pub_date=parse_date(datestring), \
            section__slug__exact=section, slug__exact=slug)
        return render_to_response('stories/email_form.html',
                                  {'story': article,
                                   'form': form},
                                   context_instance=RequestContext(request))
    elif request.method == "POST":
        form = EmailStoryForm(request.POST)
        if form.is_valid():
            sender = form.cleaned_data['sender']
            email = form.cleaned_data['email']
            user_msg = form.cleaned_data['message']
            article = Story.objects.get(issue__pub_date=parse_date(datestring), \
                section__slug__exact=section, slug__exact=slug)
            # check outgoing message for spam via Akismet and block if necessary
            from akismet import Akismet
            akismet_api = Akismet(key=settings.AKISMET_API_KEY,
                                  blog_url='http://%s/' % Site.objects.get_current().domain)
            if akismet_api.verify_key():
                akismet_data = {'comment_type': 'comment',
                                 'referrer': '',
                                 'user_ip': request.META.get('REMOTE_ADDR'),
                                 'user_agent': ''}
                if akismet_api.comment_check(user_msg.encode('utf-8'), data=akismet_data, \
                    build_data=True):
                    return render_to_response('stories/email_spam.html',
                                              {'story': article},
                                              context_instance=RequestContext(request))
                else:
                    # email stuff
                    subject = "%s has sent you an article from the Queen's Journal" % sender
                    message_template = loader.get_template('stories/email/email_to_person.txt')
                    message_context = Context({'story': article,
                                               'sender': sender,
                                               'user_msg': user_msg})
                    message = message_template.render(message_context)
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
                    return render_to_response('stories/email_complete.html',
                                             {'story': article},
                                             context_instance=RequestContext(request))
            #else:
            #    raise AkismetKeyError(settings.AKISMET_API_KEY, 'http://%s/' % Site.objects.get_current().domain)
        else:
            article = Story.objects.get(issue__pub_date=parse_date(datestring), \
                section__slug__exact=section, slug__exact=slug)
            return render_to_response('stories/email_form.html',
                  {'story': article,
                   'form': form},
                   context_instance=RequestContext(request))

''' ------------  ARCHIVES ------------- '''


# TODO: move archive views to archive apps
def index_issue_front(request, datestring):
    issue = get_object_or_404(Issue, pub_date=parse_date(datestring))
    sections = issue.sections.get_sections()
    stories = {}
    for section in sections:
        stories[section.slug] = Story.published.filter(section=section,
            issue=issue)
    if request.session.get('vote') is None:
        request.session['vote'] = []
    return render_to_response('archives/issue_front.html', {
        'sections': sections,
        'stories': stories,
        'issue': issue
        }, context_instance=RequestContext(request))


def index_issue_section(request, datestring, section):
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


def server_error(request, template_name='500.html'):
    return render_to_response(template_name, context_instance=RequestContext(request))
