# Create your views here.
from datetime import date
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import Context, RequestContext, loader
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.sites.models import Site
from django.views.generic.list_detail import object_list
from tagging.models import Tag, TaggedItem
from stories.models import Story, StoryAuthor, Photo
from blog.models import Entry
from structure.models import *

def parse_date(datestring):
	return date(*[int(x) for x in datestring.split('-')])
	
def get_issue(request):
	section = 'news'
	issue = get_object_or_404(Issue, pk=request.GET.get('issue', ''))
	return HttpResponseRedirect('/story/%s/' % issue.pub_date)
	
def index_latest(request):
	try:
		issue = Issue.objects.pub_date.latest()
	except:
		issue = FrontPageConfig.objects.latest('pub_date')
	return index_front(request, issue.pub_date.strftime("%Y-%m-%d"))
	
def index_section(request, section):
	section_config = get_object_or_404(SectionFrontConfig, section__slug__iexact=section)
	if section_config.template:
		template = section_config.template
	else:
		template = 'stories/index_section.html'
	featured = Story.objects.filter(section__slug__iexact=section, featured=True, status='p').exclude(storyphoto__isnull=True, gallery__isnull=True).order_by('-pub_date')[:5]
	for story in featured:
		if story.gallery_set.all:
			story.first_photo = Photo.objects.filter(gallery__story=story)[0]
	story_set = Story.objects.filter(section__slug__iexact=section, status='p').order_by('-pub_date')
	latest_stories = story_set[:5]
	other_stories = story_set[5:13]
	if request.session.get('vote') is None:
		request.session['vote'] = []
	return render_to_response(template,
							{'featured': featured,
							'latest_stories': latest_stories,
							'other_stories': other_stories,
							'config': section_config},
							context_instance=RequestContext(request))
							
def index_front(request):
	front_config = FrontConfig.objects.latest('pub_date')
	latest_stories = Story.objects.filter(status='p').order_by('-pub_date')[:5]
	latest_entries = Entry.objects.filter(is_published=True).order_by('-date_published')[:10]
	latest_section = []
	for section in front_config.sections.flatplansection_set.all():
		latest_section.extend(Story.objects.filter(section=section.section, featured=True)[:1])
	if request.session.get('vote') is None:
		request.session['vote'] = []
	return render_to_response('stories/index_front.html',
							{'featured': front_config.featuredstory_set.all(),
							'latest_stories': latest_stories,
							'latest_entries': latest_entries,
							'latest_section': latest_section,
							'config': front_config},
							context_instance=RequestContext(request))
							
def index_issue_front(request, datestring):
	issue = get_object_or_404(Issue, pub_date=parse_date(datestring))
	try:
		front_config = FrontPageConfig.objects.get(issue=issue)
	except FrontPageConfig.DoesNotExist:
		front_config = FrontConfig.objects.get(issue=issue)
	featured = Story.objects.filter(status='p', issue=issue, section_order=1).exclude(storyphoto__isnull=True).order_by('-pub_date')[:5]
	latest_stories = Story.objects.filter(status='p', issue=issue).order_by('-pub_date')[:5]
	back_issue = True
	latest_section = []
	for section in issue.sections.flatplansection_set.all():
		latest_section.extend(Story.objects.filter(section=section.section, issue=issue)[:1])
	if request.session.get('vote') is None:
		request.session['vote'] = []
	return render_to_response('stories/index_front_archive.html',
							  {'featured': featured,
								'latest_stories': latest_stories,
								'latest_section': latest_section,
								'config': front_config,
								'back_issue': back_issue,
								'issue': issue},
							  context_instance=RequestContext(request))
						
def index_issue_section(request, datestring, section):
	issue = get_object_or_404(Issue, pub_date=parse_date(datestring))
	try:
		front_config = FrontPageConfig.objects.get(issue=issue)
	except FrontPageConfig.DoesNotExist:
		front_config = FrontConfig.objects.get(issue=issue)
	section_config = get_object_or_404(SectionFrontConfig.objects.filter(section__slug__iexact=section))
	first_story = Story.objects.filter(section__slug__iexact=section, issue=issue, status='p').exclude(storyphoto__isnull=True).order_by('section_order')
	story_set = Story.objects.filter(issue=issue, section__slug__iexact=section).order_by('section_order')
	back_issue = True
	featured = []
	try:
		if first_story[0]:
			featured = first_story[0]
			other_stories = story_set[1:]	
	except IndexError:
		other_stories = story_set
	last_story = other_stories.reverse()[0]
	older_stories = Story.objects.filter(section__slug__iexact=section, pub_date__lt=last_story.pub_date).order_by('-pub_date')[:5]
	if request.session.get('vote') is None:
		request.session['vote'] = []
	return render_to_response('stories/index_section_archive.html',
							{'featured': featured,
							'other_stories': other_stories,
							'older_stories': older_stories,
							'config': front_config,
							'section_config': section_config,
							'back_issue': back_issue,
							'issue': issue},
							context_instance=RequestContext(request))		
'''
def index_section_latest(request, section):
	try:
		config = FlatPlanConfig.objects.filter(flatplansection__section__slug=section)
		issue = Issue.objects.published().filter(section__in=list(configs)).latest()
	except Issue.DoesNotExist, FlatPlanConfig.DoesNotExist:
		raise Http404
	return HttpResponseRedirect('/story/%s/%s/' % (issue.pub_date.strftime("%Y-%m-%d"), section))
'''	
def detail_story(request, datestring, section, slug):
	story_selected = get_object_or_404(Story, issue__pub_date=parse_date(datestring), section__slug__exact=section, slug__exact=slug)
	if request.session.get('vote') is None:
		request.session['vote'] = []
	return render_to_response('stories/single_detail.html',
								{'story': story_selected},
								context_instance=RequestContext(request))
								
def detail_author(request, author):
	curr_author = get_object_or_404(Author, slug__exact=author)
	story_set = StoryAuthor.objects.filter(author__slug__exact=author).order_by('-pub_date')
	entry_set = Entry.objects.filter(author__slug__exact=author).order_by('-date_published')
	if request.session.get('vote') is None:
		request.session['vote'] = []
	return render_to_response('stories/author_detail.html',
								{'author': curr_author,
								'stories': story_set,
								'entries': entry_set,},
								context_instance=RequestContext(request))
								
def tags(request):
	return render_to_response("tags/tags.html", context_instance=RequestContext(request))
	
def with_tag(request, tag, object_id=None, page=1): 
	
	unslug = tag.replace('-', ' ')
	query_tag = Tag.objects.get(name=unslug)
	stories = TaggedItem.objects.get_by_model(Story, query_tag)
	stories = stories.order_by('-pub_date') 

	return render_to_response("tags/with_tag.html", {'tag': tag, 
								'stories': stories},
								context_instance=RequestContext(request))