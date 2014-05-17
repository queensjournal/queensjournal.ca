import datetime

from django.db import models
from .managers import StoryManager

from tagging.fields import TagField
from tagging.models import Tag


STATUS_CHOICES = (
    ('d', 'Draft'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
)


class Story(models.Model):
    title = models.CharField(max_length=255)
    deck = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(
        help_text='Automatically written based on the headline. If nothing \
            shows up here, try typing in the headline instead of copying and \
            pasting.')
    section = models.ForeignKey('sections.Section')
    issue = models.ForeignKey('issues.Issue', null=True, blank=True)
    label = models.CharField(max_length=255, blank=True, null=True,
        editable=False)
    content = models.TextField()
    summary = models.TextField(
        help_text='Sum up the story in a single paragraph.')
    section_order = models.PositiveSmallIntegerField("Order in section",
        help_text="Determines the order of all stories in the section, with \
            lower numbers at the top (so a story with order priority 1 would \
            be at the top).", editable=False, null=True)
    enable_comments = models.BooleanField(default=True)
    show_headshots = models.BooleanField(default=False,
        help_text="Check when you want to display headshots. For Ops pieces \
            and Signed Eds.")
    tags = TagField(blank=True,
        help_text='Article Tags and Label. Use this to apply tags to the \
            story. Use commas to separate tags. The first tag will be the \
            story\'s label. For example: \"Student Ghetto, EngSoc, Town-Gown, \
            Aberdeen\"')
    featured = models.BooleanField(help_text="Checking this will feature this \
        story on its respective section page. The most recent featured story \
        from each section will be placed on the Front page.")
    pub_date = models.DateTimeField(default=datetime.datetime.now, unique=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES,
        default='d',
        help_text='Draft will place the story in a queue to be published \
            later, published will publish the story immediately.')
    is_tweeted = models.BooleanField(editable=False, default=False)
    is_published = models.BooleanField(editable=False)

    photos = models.ManyToManyField('Photo', through='StoryPhoto')
    authors = models.ManyToManyField('authors.Author', through='StoryAuthor')
    galleries = models.ManyToManyField('galleries.Gallery',
        related_name='story')

    objects = StoryManager()

    class Meta:
        verbose_name_plural = "Stories"
        get_latest_by = 'pub_date'
        ordering = ['-pub_date']

    def story_thumb(self):
        if self.show_headshots is True:
            try:
                sa = StoryAuthor.objects.filter(story=self)[0]
                return sa.author.headshot
            except IndexError:
                return False
        if self.galleries.all():
            try:
                return self.galleries.all()[0].images.all()[0].photo
            except IndexError:
                return False
        else:
            try:
                sp = StoryPhoto.objects.filter(story=self)[0]
                return sp.photo
            except IndexError:
                return False

    def story_photo(self):
        from galleries.models import Gallery
        if self.gallery_set.all():
            try:
                gallery = Gallery.objects.filter(story=self)[0]
                return gallery.images.all()[0]
            except IndexError:
                return False
        else:
            try:
                sp = StoryPhoto.objects.filter(story=self)[0]
                return sp.photo
            except IndexError:
                return False

    def first_photo(self):
        sp = StoryPhoto.objects.filter(story=self)[0]
        return sp.photo

    def other_photos(self):
        if len(self.storyphoto_set.all()) > 1:
            return StoryPhoto.objects.filter(story=self).exclude(
                photo=self.first_photo)

    def related_photos(self):
        return StoryPhoto.objects.filter(story=self)

    def has_inlines(self):
        inline_models = models.get_app("inlines")
        for obj_type in models.get_models(inline_models):
            inlines = obj_type.objects.filter(story=self)
            if len(inlines) > 0:
                return True
            else:
                return False

    def has_wide_inlines(self):
        inline_models = models.get_app("inlines")
        for obj_type in models.get_models(inline_models):
            inlines = obj_type.objects.filter(story=self, full_width=True)
            if len(inlines) > 0:
                return True
            else:
                return False

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def label(self):
        return self.section

    def get_tags(self, tags):
        return Tag.objects.get_for_object(self)

    def model_type(self):
        return self.__class__.__name__

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.status == 'p':
            self.is_published = True
        super(Story, self).save(*args, **kwargs)

    def get_datestring(self):
        return self.pub_date.strftime("%Y-%m-%d")

    @models.permalink
    def get_absolute_url(self):
        return ('story-detail', (), {
                'datestring': self.get_datestring(),
                'section': self.section.slug,
                'slug': self.slug,
                'pk': self.pk,
                })

    def get_twitter_message(self):
        return u'%s: %s' % (self.title, self.summary)


class StoryAuthor(models.Model):
    author = models.ForeignKey('authors.Author', default=None)
    story = models.ForeignKey(Story)

    class Meta:
        order_with_respect_to = 'story'

    def __unicode__(self):
        return '%s - %s' % (self.author.name, self.story.title)


class Photo(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(
        help_text='Automatically written based on the headline. If nothing \
            shows up here, try typing in the headline instead of copying and \
            pasting.')
    image = models.ImageField(upload_to='story_photos/%Y/%m/%d/',
        help_text='Please convert all images to RGB JPEGs.')
    thumbnail = models.ImageField(upload_to='thumbs/', editable=False,
        null=True, default='')
    issue = models.ForeignKey('issues.Issue', blank=True, null=True)
    caption = models.TextField(blank=True)
    photographer = models.ForeignKey('authors.Author', blank=True, null=True)
    credit = models.CharField("Optional credit", max_length=255,
        help_text="For special photo credits not involving a staff \
            photographer, ex. 'Photo supplied by Queen's Alumni Services,' \
            'Journal File Photo,' etc.", blank=True)
    creation_date = models.DateField(default=datetime.date.today())

    def thumbnail(self):
        return '<img src="%s"/>' % (self.thumbnail_image.url)
    thumbnail.short_description = 'Image thumbnail'
    thumbnail.allow_tags = True

    def photo_stories(self):
        from django.core import urlresolvers
        storyp_set = StoryPhoto.objects.filter(photo=self)
        sections = []
        for storyp in storyp_set:
            url = urlresolvers.reverse('admin:stories_story_change', \
                args=(storyp.story.id,))
            sections.append('<a href="%s">%s</a>' % (url, storyp.story.title))
        return ", ".join(sections)
    photo_stories.short_description = 'Locations'
    photo_stories.allow_tags = True

    def list_photographer(self):
        if self.photographer is not None:
            return '<a href="%s">%s</a>' % (
                self.photographer.get_absolute_url(), self.photographer)
        elif self.credit != '':
            return self.credit
        else:
            return '[no credit]'
    list_photographer.short_description = 'Credit'

    def get_absolute_url(self):
        return self.photo
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        return self.name


class StoryPhoto(models.Model):
    photo = models.ForeignKey(Photo, default=None)
    story = models.ForeignKey(Story)

    def thumbnail(self):
        return '<img src="%s"/>' % (self.photo.thumbnail_image.url)
    thumbnail.short_description = 'Image thumbnail'
    thumbnail.allow_tags = True

    class Meta:
        verbose_name = "Story photos"
        verbose_name_plural = "Story photos"
        order_with_respect_to = 'story'
