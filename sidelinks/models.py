from django.db import models

class SidebarLinkset(models.Model):
    name = models.CharField(max_length=255, help_text='The internal name of this linkset.')
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

class Link(models.Model):
    text = models.CharField(max_length=255, help_text='The text of the sidebar link.')
    url = models.CharField(max_length=255, help_text='The URL of the sidebar link.')
    active = models.BooleanField(default=True, help_text='Active link. Turn this off to \
        remove a link from the sidebar instead of deleting it.')
    css_class = models.CharField(max_length=100, help_text='CSS classes for the link', \
        null=True, blank=True)
    sidebar = models.ForeignKey(SidebarLinkset)

    class Meta:
        order_with_respect_to	= 'sidebar'
