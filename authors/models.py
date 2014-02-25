from django.db import models
from django.contrib.auth.models import User


class Headshot(models.Model):
    name = models.SlugField()
    headshot = models.ImageField(upload_to="headshots/%Y/",
        help_text='Please crop all photos to 200x100 pixels and convert them \
            to RGB JPG.', null=True, blank=True)

    def __unicode__(self):
        return self.name


class AuthorRole(models.Model):
    start_date = models.DateField()
    position = models.CharField(max_length=64)
    author = models.ForeignKey('authors.Author')

    class Meta:
        get_latest_by = 'start_date'
        ordering = ['-start_date']

    def __unicode__(self):
        return self.author.name


class Author(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField()
    email = models.EmailField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    headshot = models.ForeignKey('Headshot', null=True, blank=True)
    homepage = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    @models.permalink
    def get_absolute_url(self):
        return ('author-detail', [self.slug])

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
