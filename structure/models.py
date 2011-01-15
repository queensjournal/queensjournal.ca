from django.db import models
from django.contrib.auth.models import User
from polls.models import Poll

class Author(models.Model):
	name = models.CharField(max_length=64, unique=True)
	user = models.ForeignKey(User)
	
	def get_latest_role(self):
		if self.authorrole_set:
			return self.authorrole_set.latest().position
		return ''
	get_latest_role.short_description = 'Current/last title'

	def get_latest_role_date(self):
		if self.authorrole_set:
			return self.authorrole_set.latest().start_date
		return ''
	get_latest_role_date.short_description = 'Title held since'

	def get_role(self, date):
		"""
		Returns the author's job title at a specific date.
		"""
 		if self.authorrole_set:
			roles_before = self.authorrole_set.filter(start_date__lte=date)
			if roles_before.count() > 0:
			    return roles_before.order_by('-start_date')[0].position
			else:
			    return ''
		return ''

	def __unicode__(self):
		return self.name
		
class Volume(models.Model):
	volume = models.PositiveSmallIntegerField(unique=True)
	
	def get_years(self):
		"""
		Returns a DateQuerySet containing the year span for all issues in the volume
		"""
		return self.issue_set.dates('pub_date', 'year')
		
	def __unicode__(self):
		return '%i' % (self.volume,)

class Section(models.Model):
	name = models.CharField(max_length=100, unique=True)
	short_name = models.CharField(max_length=16, help_text='For use in site navigation like section menus, breadcrumb, etc. Optional.', blank=True, null=True)
	slug = models.SlugField()
	def __unicode__(self):
		return self.name

class Volume(models.Model):
	volume = models.PositiveSmallIntegerField(unique=True)
	def get_years(self):
		return self.issue_set.dates('pub_date', 'year')
	def __unicode__(self):
		return '%i' % (self.volume,)
	
class Issue(models.Model):
	issue = models.PositiveSmallIntegerField()
	volume = models.ForeignKey(Volume)
	pub_date = models.DateField("Publication Date", unique=True)
	sections = models.ForeignKey('FlatPlanConfig')
	extra = models.CharField('Extra', help_text='Use for "Special Issue of the Journal" e.g. a Vanier Cup win, AMS Election, etc.', max_length='255', blank=True, null=True)
	def __unicode__(self):
		if self.extra != "":
			return 'Vol. %s, %s (special issue)' % (self.volume, self.extra)
		else:
			return 'Vol. %s, Issue %i' % (self.volume, self.issue)

class FlatPlanConfig(models.Model):
	name = models.CharField(max_length=255, help_text='Descriptive name for the flatplan configuration (ex. \'Vol. 135 standard\', \'Vol. 135 with Supplement\', \'Vol. 136 Extra\'.')
	
	def list_sections(self):
		sections = []
		section_qset = list(self.flatplansection_set.all())
		for section_wrapper in section_qset:
		    if section_wrapper != section_qset[-1]:
		        sections.append(section_wrapper.section.name + ',')
		    else:
		        sections.append(section_wrapper.section.name)
		return ' '.join(sections)
	list_sections.short_description = 'Section order'

	def array_sections(self):
		sections = []
		section_qset = list(self.flatplansection_set.all())
		for section_wrapper in section_qset:
		    sections.append(section_wrapper.section)
		return sections
		
	class Meta:
		verbose_name = 'Issue Configuration'
		verbose_name_plural = 'Issue Configurations'

	def __unicode__(self):
		return self.name
		
class FlatPlanSection(models.Model):
	section = models.ForeignKey(Section, default=None)
	config = models.ForeignKey(FlatPlanConfig)

	class Meta:
		order_with_respect_to = 'config'
		
class FrontPageConfig(models.Model):
	from journal.stories.models import Story
	poll = models.ForeignKey(Poll, blank=True, null=True)
	announce_head = models.CharField("Announcement headline", max_length=255, blank=True)
	announce_body = models.TextField("Announcement text", blank=True)
	pub_date = models.DateTimeField("Layout Date")
	
	class Meta:
		verbose_name = 'Front Page Layout'
		
	def __unicode__(self):
		return self.pub_date.strftime("%Y-%m-%d")