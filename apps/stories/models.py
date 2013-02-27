import datetime
from django.db import models
from stories.managers import PublishedStoryManager
from structure.models import Issue, Section, Author
from imagekit.models import ImageModel
from tagging.fields import TagField
from tagging.models import Tag


STATUS_CHOICES = (
    ('d', 'Draft'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
)


class Story(models.Model):
    head = models.CharField(max_length=255)
    deck = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(
        help_text='Automatically written based on the headline. If nothing \
            shows up here, try typing in the headline instead of copying and \
            pasting.')
    section = models.ForeignKey(Section)
    issue = models.ForeignKey(Issue, null=True, blank=True)
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
    featured = models.BooleanField()
    pub_date = models.DateTimeField(default=datetime.datetime.now, unique=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES,
        default='d',
        help_text='Draft will place the story in a queue to be published \
            later, published will publish the story immediately.')
    is_tweeted = models.BooleanField(editable=False, default=False)
    is_published = models.BooleanField(editable=False)

    objects = models.Manager()
    published = PublishedStoryManager()

    class Meta:
        verbose_name_plural = "Stories"
        get_latest_by = 'pub_date'
        ordering = ['-pub_date']

    def list_authors(self):
        authors = []
        author_qset = list(self.storyauthor_set.all())
        author_num = len(author_qset)
        # byline names
        for wrapper in author_qset:
            if (author_num > 1 and wrapper != author_qset[-2]) \
            or author_num == 1:
                authors.append('<a href="/author/%s/">%s</a>, ' % (
                    wrapper.author.slug, wrapper.author.name))
            else:
                authors.append('<a href="/author/%s/">%s</a>' % (
                    wrapper.author.slug, wrapper.author.name))

        # byline titles
        if author_num > 1:
            authors.insert(-1, 'and')
            authors.append('Journal Staff')
        elif author_num == 1:
            authors.append(author_qset[0].author.get_role(self.pub_date))
        elif author_num == 0:
            authors.append('Journal Staff')
        return ' '.join(authors)
    list_authors.short_description = 'Author(s)'

    def story_thumb(self):
        from galleries.models import Gallery
        if self.show_headshots is True:
            try:
                sa = StoryAuthor.objects.filter(story=self)[0]
                return sa.author.headshot
            except IndexError:
                return False
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

    def get_tags(self, tags):
        return Tag.objects.get_for_object(self)

    def model_type(self):
        return self.__class__.__name__

    def __unicode__(self):
        return self.head

    def save(self, *args, **kwargs):
        if self.status == 'p':
            self.is_published = True
        super(Story, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('stories.views.detail_story', (), {
            'datestring': self.pub_date.strftime("%Y-%m-%d"),
            'section': self.section.slug,
            'slug': self.slug})

    def get_twitter_message(self):
        return u'%s: %s' % (self.head, self.summary)


class StoryAuthor(models.Model):
    author = models.ForeignKey(Author, default=None)
    story = models.ForeignKey(Story)

    class Meta:
        order_with_respect_to = 'story'

    def __unicode__(self):
        return '%s - %s' % (self.author.name, self.story.head)


class Photo(ImageModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(
        help_text='Automatically written based on the headline. If nothing \
            shows up here, try typing in the headline instead of copying and \
            pasting.')
    photo = models.ImageField(upload_to='story_photos/%Y/%m/%d/',
        help_text='Please convert all images to RGB JPEGs.')
    thumbnail = models.ImageField(upload_to='thumbs/', editable=False,
        null=True, default='')
    issue = models.ForeignKey(Issue, blank=True, null=True)
    caption = models.TextField(blank=True)
    photographer = models.ForeignKey(Author, blank=True, null=True)
    credit = models.CharField("Optional credit", max_length=255,
        help_text="For special photo credits not involving a staff \
            photographer, ex. 'Photo supplied by Queen's Alumni Services,' \
            'Journal File Photo,' etc.", blank=True)
    creation_date = models.DateField(default=datetime.date.today())

    class IKOptions:
        # Defining ImageKit options
        spec_module = 'stories.specs'
        cache_dir = 'photo_cache'
        image_field = 'photo'

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
            head = storyp.story.head
            sections.append('<a href="%s">%s</a>' % (url, head))
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
