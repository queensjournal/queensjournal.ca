import datetime
from django.db import models
from django.db.models import Q
from structure.models import Issue, Author
from stories.models import Story, Photo
from imagekit.models import ImageModel

class PreviousStories:
    """
    Not actually a QuerySet Manager, but a class designed to provide manager-like
    functionality for the "previous stories" sidebar.
    """
    def __init__(self, section, num):
        self.section, self.num = section, num

    def get_future(self):
        latest = Issue.objects.published().latest()
        return Story.objects.select_related().filter(issue__pub_date__lt=latest.pub_date, \
            section=self.section).order_by('-structure_issue.pub_date')[:self.num]

    def get_by_issue(self, issue):
        return Story.objects.select_related().filter(issue__pub_date__lt=issue.pub_date, \
            section=self.section).order_by('-structure_issue.pub_date')[:self.num]


class CalendarSidebarManager(models.Manager):
    def get_by_issue(self, issue):
        """
        Takes an Issue object and returns all calendar items for the week
        following the publication date of the issue.
        """
        return self.get_query_set().filter(start_time__gte=issue.pub_date).filter(\
            start_time__lt=Issue.objects.next(issue).pub_date)

    def get_future(self):
        """
        Returns events in the future, calculated based on the current datetime.
        """
        return self.get_query_set().filter(Q(end_time__gte=datetime.datetime.now()) | \
            (Q(end_time__isnull=True) & Q(start_time__gte=datetime.datetime.now())))


class SportsSidebarManager(models.Manager):
    def get_by_issue(self, issue):
        """
        Takes an Issue object and returns all calendar items for the week
        following the publication date of the issue.
        """
        try:
            return self.get_query_set().filter(start_time__lte=issue.pub_date).filter(\
                start_time__gte=issue.get_previous_by_pub_date().pub_date)
        except:
            return self.get_query_set().filter(start_time__lte=issue.pub_date)

    def get_future(self):
        """
        Returns events in the future, calculated based on the current datetime.
        """
        try:
            latest = Issue.objects.published().latest()
        except:
            return None
        return self.get_query_set().filter(start_time__gte=latest.pub_date - \
            datetime.timedelta(7))


class StaticSidebarManager(models.Manager):
    def get_by_issue(self, issue):
        return self.get_query_set().filter(issue=issue)

    def get_future(self):
        try:
            latest = Issue.objects.published().latest()
        except:
            return None
        return self.get_query_set().filter(issue=latest)


class NewsCalendarItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True, default=None)
    location = models.CharField(max_length=255)
    event_type = models.ForeignKey('EventType', help_text='Not currently in use for \
        NewsCalendarItem.', blank=True, null=True)
    objects = CalendarSidebarManager()

    class Meta:
        ordering            = ('start_time','end_time')

    def __unicode__(self):
        return self.name


class ArtsCalendarItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateField(help_text='Beginning of period for which \
        showtimes apply.')
    end_time = models.DateField(blank=True, null=True, default=None, help_text='End of \
        period for which showtimes apply. Optional.')
    location = models.CharField(max_length=255)
    event_type = models.ForeignKey('EventType')
    objects = CalendarSidebarManager()

    class Meta:
        ordering            = ('event_type','location','name','start_time')

    def __unicode__(self):
        return self.name


class ArtsCalendarShowtime(models.Model):
    time = models.TimeField()
    item = models.ForeignKey(ArtsCalendarItem)

    class Meta:
        verbose_name        = 'Event Showtime'
        ordering            = ('time',)


class TalkingHeadsItem(models.Model):
    question = models.CharField(max_length=255)
    location = models.CharField("at...", max_length=255, help_text="ex. \
        'the Common Ground', 'Jock Harty Arena', '368 Brock Street'")
    issue = models.ForeignKey(Issue, unique=True)
    objects = StaticSidebarManager()
    photos_by = models.ForeignKey(Author, null=True)

    def list_photographers(self):
        photogs = []
        name_in_list = False
        for answer in self.talkingheadsanswer_set.all():
            for photog in photogs:
                try:
                    if answer.photo.photographer.name == photog:
                        name_in_list = True
                        break
                except:
                    continue
            if name_in_list is False:
                try:
                    photogs.append(answer.photo.photographer.name)
                except:
                    continue
            name_in_list = False
        if len(photogs) > 2:
            for i in range(len(photogs)-2):
                photogs[i] = photogs[i] + ","
        if len(photogs) > 1:
            photogs[-1:-1] = ['and']
        return ' '.join(photogs)

    class Meta:
        ordering = ['issue']


class TalkingHeadsAnswer(ImageModel):
    name = models.CharField(max_length=255)
    quote = models.TextField()
    photo = models.ForeignKey(Photo, help_text="Photos should be 100 pixels square. \
        JPEGs only, please.", editable=False, null=True)
    image = models.ImageField(upload_to='talking_heads/%Y/%m/%d/', help_text="Photos \
        should be square. JPEGs only, please.")
    question = models.ForeignKey(TalkingHeadsItem)

    class IKOptions:
        # Defining ImageKit options
        spec_module = 'sidebars.heads_specs'
        cache_dir = 'photo_cache'
        image_field = 'image'

    class Meta:
        order_with_respect_to   = 'question'


class EventType(models.Model):
    event_type = models.CharField(max_length=255)

    def __unicode__(self):
        return self.event_type


##class Announcement(models.Model):
##    head = models.CharField(max_length=255)
##    blurb = models.TextField()
##    start_date = models.DateField()
##    end_date = models.DateField()


class SportsCalendarItem(models.Model):
    sport = models.ForeignKey('SportType')
    start_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    ticket_info = models.TextField(blank=True)
    objects = SportsSidebarManager()

    def is_played(self):
        return self.start_time < datetime.datetime.now()

    class Admin:
        fields = (
            ('Pre-event info', {
                'fields': ('sport', 'start_time', 'location', 'ticket_info'),
                'description': 'For team events, fill in the pre-event info and the two \
                    teams under "Team Result." For individual events, fill in the \
                    pre-event info and leave "Individual Results" blank. After the \
                    game/event is over, fill in the results as needed. If you require \
                    more fields for individual results, click "Save and continue editing" \
                    after filling out all available result fields.'
            }),
        )
        list_display        = ('sport', 'location', 'start_time', 'is_played')
        list_filter         = ('start_time', 'sport')
        ordering            = ('-start_time',)

    class Meta:
        ordering            = ('start_time', 'sport')

    def __unicode__(self):
        if self.sportsteamgamescore_set.count() == 0:
            return "%s @ %s, %s" % (self.sport.name, self.location, self.start_time)
        else:
            teams = self.sportsteamgamescore_set.all()[0]
            return "%s, %s vs. %s, %s" % (self.sport.name, teams.home_team, \
                teams.away_team, self.start_time)


class SportsTeamGameScore(models.Model):
    home_team = models.CharField(max_length=255)
    home_score = models.PositiveSmallIntegerField(blank=True, null=True)
    away_team = models.CharField(max_length=255)
    away_score = models.PositiveSmallIntegerField(blank=True, null=True)
    event = models.ForeignKey(SportsCalendarItem) #, edit_inline=models.TABULAR,
        #min_num_in_admin=1, max_num_in_admin=1, num_in_admin=1, num_extra_on_change=0

    class Meta:
        verbose_name = 'Team Result'


class SportsIndividualScore(models.Model):
    event_detail = models.CharField('Individual event name', max_length=255, blank=True)
    name = models.CharField(max_length=255)
    place = models.PositiveSmallIntegerField(blank=True, null=True)
    result_detail = models.CharField(max_length=255, blank=True)
    home_team = models.BooleanField("Queen's athlete?")
    school = models.CharField("School name (if not Queen's)", max_length=255, blank=True)
    event = models.ForeignKey(SportsCalendarItem) #, edit_inline=models.TABULAR,
        # min_num_in_admin=1, num_in_admin=9, num_extra_on_change=2

    class Meta:
        verbose_name        = 'Individual Result'
        ordering            = ('event_detail', 'place')


class SportType(models.Model):
    name = models.CharField(max_length=255)

    class Admin:
        pass

    def __unicode__(self):
        return self.name
