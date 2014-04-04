from datetime import datetime
from django.db import models


class FlatPlanConfig(models.Model):
    name = models.CharField(max_length=255,
        help_text='Descriptive name for the flatplan configuration (ex. \'Vol\
            . 135 standard\', \'Vol. 135 with Supplement\', \'Vol. 136 \
            Extra\'.')

    def get_sections(self):
        sections = []
        for flat_section in self.flatplansection_set.all() \
                .prefetch_related('section'):
            sections.append(flat_section.section)
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
    section = models.ForeignKey('sections.Section', default=None)
    config = models.ForeignKey(FlatPlanConfig)
    #order = models.PositiveSmallIntegerField("Order",
        #help_text="Order ")

    class Meta:
        order_with_respect_to = 'config'

    def __unicode__(self):
        return self.section.name


class FrontConfig(models.Model):
    announce_head = models.CharField("Announcement headline", max_length=255,
        blank=True)
    announce_body = models.TextField("Announcement text", blank=True)
    pub_date = models.DateTimeField(default=datetime.now())
    sections = models.ForeignKey(FlatPlanConfig)
    issue = models.ForeignKey('issues.Issue', blank=True, null=True)

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
    issue = models.ForeignKey('issues.Issue', unique=True)
    announce_head = models.CharField("Announcement headline", max_length=255,
        blank=True)
    announce_body = models.TextField("Announcement text", blank=True)

    class Admin:
        pass

    class Meta:
        verbose_name = 'Front Page Layout'

    def __unicode__(self):
        return self.issue.__unicode__()
