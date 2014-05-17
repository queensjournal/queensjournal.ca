from django.db import models
from stories.models import Story


class Section(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=16,
        help_text='For use in site navigation like section menus, breadcrumb, \
            etc. Optional.', blank=True, null=True)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

    def get_issue_stories(self, issue):
        return Story.objects.published().filter(section=self, issue=issue)

    def get_latest_stories(self, limit=10):
        return Story.objects.published().filter(section=self)[:limit]

    def get_top_featured_story(self):
        return self.get_featured_stories()[:1].get()

    def get_featured_stories(self):
        return Story.objects.published().filter(section=self, featured=True)

    @models.permalink
    def get_absolute_url(self):
        return ('front-section', (), {'slug': self.slug})
