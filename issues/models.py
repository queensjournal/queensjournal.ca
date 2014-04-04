from django.db import models
from .managers import IssueManager


class Volume(models.Model):
    volume = models.PositiveSmallIntegerField(unique=True)
    issuu_embed = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-volume']

    def get_years(self):
        """
        Returns a DateQuerySet containing the year span for all issues in the
        volume
        """
        return self.issue_set.dates('pub_date', 'year')

    def issue_list(self):
        return self.issue_set.order_by('issue')

    @models.permalink
    def get_absolute_url(self):
        return ('archive-volume-detail', (), {
                'volume': self.volume,
                })

    def __unicode__(self):
        return 'Volume %i' % (self.volume,)


class Issue(models.Model):
    PUBLISH_STATUS_CHOICES = (
        ('PUB', 'Published'),
        ('NPB', 'Not yet published'),
    )

    issue = models.PositiveSmallIntegerField()
    volume = models.ForeignKey(Volume)
    pub_date = models.DateField("Publication Date", unique=True)
    sections = models.ForeignKey('structure.FlatPlanConfig')
    extra = models.CharField('Extra',
        help_text='Use for "Special Issue of the Journal" e.g. a Vanier Cup \
            win, AMS Election, etc.', max_length='255', blank=True, null=True)
    is_published = models.CharField('Publish status', max_length=3,
        choices=PUBLISH_STATUS_CHOICES, default='NPB')

    objects = IssueManager()

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

    @models.permalink
    def get_absolute_url(self):
        return ('issue-detail', (), {
            'volume': self.volume.volume,
            'issue': self.issue,
        })

    def __unicode__(self):
        if self.extra != "":
            return 'Vol. %s, %s (special issue)' % (self.volume.volume,
                self.extra)
        else:
            return 'Vol. %s, Issue %i' % (self.volume.volume, self.issue)

    def get_featured_stories(self):
        stories = []
        for section in self.sections.flatplansection_set.all():
            stories.append(section.section.get_top_featured_story())
        return stories
