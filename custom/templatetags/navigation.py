from django import template
from structure.models import Issue, Volume, FrontConfig
from stories.models import Story

register = template.Library()

class CurrentIssueNode(template.Node):
	"""
	Returns the latest published Issue object as a context variable.
	"""
	def __init__(self, varname):
		self.varname = varname

	def render(self, context):
		context[self.varname] = Issue.objects.pub_date.get_latest_by()
		return ''

def do_current_issue(parser, token):
	"""
	{% current_issue as issue %}
	"""
	bits = token.contents.split()
	if len(bits) != 3:
		raise template.TemplateSyntaxError, "'%s' tag takes two arguments" % bits[0]
	if bits[1] != 'as':
		raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
	return CurrentIssueNode(bits[2])

class IssueArchivesNode(template.Node):
	"""
	Returns the list of published Issue objects as a context variable.
	"""
	def __init__(self, varname):
		self.varname = varname

	def render(self, context):
		context[self.varname] = Issue.objects.order_by('-pub_date')
		return ''

def do_issue_archives(parser, token):
	"""
	{% issue_archives as issues %}
	"""
	bits = token.contents.split()
	if len(bits) != 3:
		raise template.TemplateSyntaxError, "'%s' tag takes two arguments" % bits[0]
	if bits[1] != 'as':
		raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
	return IssueArchivesNode(bits[2])

def menu_sections(context):
	"""
	Returns the HTML code for the sections menu of a given issue.
	"""
	params = {}
	latest_issue = FrontConfig.objects.latest('pub_date')
	if context.get('story_set'):
		params['show_section_link'] = False
	else:
		params['show_section_link'] = True
	params['sections'] = latest_issue.sections
	return params

class OtherStoriesListNode(template.Node):
	"""
	Returns a list of other stories in the section for a given issue as the 'other_stories' context variable.
	"""
	def __init__(self, section, issue, num=0):
		self.section, self.issue, self.num = section, issue, num

	def render(self, context):
		# first, grab actual section/issue objects from context
		try:
			section_obj = template.resolve_variable(self.section, context)
			issue_obj = template.resolve_variable(self.issue, context)
		except:
			context['no_other_stories'] = True
			return ''
		context['other_stories'] = Story.objects.filter(issue=issue_obj, section=section_obj).exclude(slug=context.get('story').slug)
		if self.num != 0:
			context['other_stories'] = context['other_stories'][:self.num]
		if len(context['other_stories']) == 0:
			context['no_other_stories'] = True
		return ''

def do_other_stories(parser, token):
	"""
	{% other_stories section_obj issue_obj num %}
	"""
	bits = token.contents.split()
	if len(bits) != 3 and len(bits) != 4:
		raise template.TemplateSyntaxError, "%s takes two or three arguments" % bits[0]
	if len(bits) == 4:
		return OtherStoriesListNode(bits[1], bits[2], bits[3])
	else:
		return OtherStoriesListNode(bits[1], bits[2])

	
register.tag('current_issue', do_current_issue)
register.tag('issue_archives', do_issue_archives)
register.inclusion_tag('global/menu_sections.html', takes_context=True)(menu_sections)
register.tag('other_stories', do_other_stories)
