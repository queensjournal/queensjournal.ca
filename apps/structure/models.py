from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageModel

from structure.managers import IssueManager


class Headshot(ImageModel):
    name = models.SlugField()
    headshot = models.ImageField(upload_to="headshots/%Y/",
        help_text='Please crop all photos to 200x100 pixels and convert them \
            to RGB JPG.', null=True, blank=True)

    class IKOptions:
        spec_module = 'structure.headshot_specs'
        cache_fir = 'photo_cache'
        image_field = 'headshot'

    def __unicode__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField()
    email = models.EmailField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    headshot = models.ForeignKey(Headshot, null=True, blank=True)
    homepage = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    @models.permalink
    def get_absolute_url(self):
        return ('masthead.views.detail_author', (), {
            'author': self.slug})

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


class AuthorRole(models.Model):
    start_date = models.DateField()
    position = models.CharField(max_length=64)
    author = models.ForeignKey(Author)

    class Meta:
        get_latest_by = 'start_date'
        ordering = ['-start_date']

    def __unicode__(self):
        return self.author.name


class Volume(models.Model):
    volume = models.PositiveSmallIntegerField(unique=True)
    issuu_embed = models.TextField(null=True, blank=True)

    def get_years(self):
        """
        Returns a DateQuerySet containing the year span for all issues in the
        volume
        """
        return self.issue_set.dates('pub_date', 'year')

    def __unicode__(self):
        return '%i' % (self.volume,)


class Section(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=16,
        help_text='For use in site navigation like section menus, breadcrumb, \
            etc. Optional.', blank=True, null=True)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name


class Issue(models.Model):
    PUBLISH_STATUS_CHOICES = (
        ('PUB', 'Published'),
        ('NPB', 'Not yet published'),
    )

    issue = models.PositiveSmallIntegerField()
    volume = models.ForeignKey(Volume)
    pub_date = models.DateField("Publication Date", unique=True)
    sections = models.ForeignKey('FlatPlanConfig')
    extra = models.CharField('Extra',
        help_text='Use for "Special Issue of the Journal" e.g. a Vanier Cup \
            win, AMS Election, etc.', max_length='255', blank=True, null=True)
    is_published = models.CharField('Publish status', max_length=3,
        choices=PUBLISH_STATUS_CHOICES, default='NPB')

    objects = IssueManager()

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

    def __unicode__(self):
        if self.extra != "":
            return 'Vol. %s, %s (special issue)' % (self.volume, self.extra)
        else:
            return 'Vol. %s, Issue %i' % (self.volume, self.issue)


class FlatPlanConfig(models.Model):
    name = models.CharField(max_length=255,
        help_text='Descriptive name for the flatplan configuration (ex. \'Vol\
            . 135 standard\', \'Vol. 135 with Supplement\', \'Vol. 136 \
            Extra\'.')

    def get_sections(self):
        sections = []
        section_qset = self.flatplansection_set.all()
        for section_wrapper in section_qset:
            sections.append(section_wrapper.section)
        return sections

    def list_sections(self):
        sections = []
        section_qset = list(self.flatplansection_set.all())
        for section_wrapper in section_qset:
            if section_wrapper != section_qset[-1]:
                sections.append(section_wrapper.section.name + ',')
            else:
                sections.append(section_wrapper.section.name)
        return ' '.join(sections)

    class Meta:
        verbose_name = 'Issue Configuration'
        verbose_name_plural = 'Issue Configurations'

    def __unicode__(self):
        return self.name


class FlatPlanSection(models.Model):
    section = models.ForeignKey(Section, default=None)
    config = models.ForeignKey(FlatPlanConfig)
    #order = models.PositiveSmallIntegerField("Order",
        #help_text="Order ")

    class Meta:
        order_with_respect_to = 'config'

    def __unicode__(self):
        return self.section.name


class SectionFrontConfig(models.Model):
    # TODO: Remove this model and its dependencies. overly-complicated
    announce_head = models.CharField("Announcement headline",
        max_length=255, blank=True)
    announce_body = models.TextField("Announcement text", blank=True)
    section = models.ForeignKey(Section, unique=True)

    class Meta:
        verbose_name = "Section Front Page Layout"
        ordering = ['section']

    def __unicode__(self):
        return self.section.name


class FrontConfig(models.Model):
    announce_head = models.CharField("Announcement headline", max_length=255,
        blank=True)
    announce_body = models.TextField("Announcement text", blank=True)
    pub_date = models.DateTimeField(default=datetime.now())
    sections = models.ForeignKey(FlatPlanConfig)
    issue = models.ForeignKey(Issue, blank=True, null=True)

    class Meta:
        verbose_name = "Front Layout"
        ordering = ['-pub_date']

    def __unicode__(self):
        if self.issue:
            return '%s - %s' % (
                self.pub_date.strftime("%A, %b %d, %Y - %I:%M %p"), self.issue)
        else:
            return self.pub_date.strftime("%A, %b %d, %Y - %I:%M %p")

"""
---------- LEGACY ISSUE-BASED MODELS. KEEPS OLD URLS WORKING -------------
TODO: Remove these and clear them from DB
"""


class FrontPageConfig(models.Model):
    issue = models.ForeignKey(Issue, unique=True)
    announce_head = models.CharField("Announcement headline", max_length=255,
        blank=True)
    announce_body = models.TextField("Announcement text", blank=True)

    class Admin:
        pass

    class Meta:
        verbose_name = 'Front Page Layout'

    def __unicode__(self):
        return self.issue.__unicode__()
