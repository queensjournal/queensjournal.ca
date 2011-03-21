from django.db import models

class SidebarLinkset(models.Model):
    name = models.CharField(max_length=255, help_text='The internal name of this linkset.')
    slug = models.SlugField() #prepopulate_from=('name',)

    class Admin:
        pass

    def __unicode__(self):
        return self.name
    

class Link(models.Model):
    text = models.CharField(max_length=255, help_text='The text of the sidebar link.')
    url = models.URLField(max_length=255, verify_exists=False, help_text='The URL of the sidebar link.')
    active = models.BooleanField(default=True, help_text='Active link. Turn this off to remove a link from the sidebar instead of deleting it.')
    sidebar = models.ForeignKey(SidebarLinkset) #, edit_inline=models.TABULAR, min_num_in_admin=1, num_in_admin=6, num_extra_on_change=3

    class Meta:
        order_with_respect_to   = 'sidebar'
    
