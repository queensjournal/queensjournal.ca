from django.db import models
from stories.models import Story


class Factbox(models.Model):
    # standard inline object fields
    story = models.ForeignKey(Story)

    # Factbox fields
    head = models.CharField(max_length=255)
    full_width = models.BooleanField("Full-width factbox (for tables, etc.)", default=False)
    body = models.TextField()
    source = models.CharField("Source credit line", max_length=255, blank=True)

##    class Admin:
##        list_display        = ('name', 'head')
##        list_filter         = ('created',)
##        search_fields       = ('name', 'head', 'body')

    class Meta:
        verbose_name_plural = "Factboxes"

    def __unicode__(self):
        return self.head


class Document(models.Model):
    # standard inline object fields
    story = models.ForeignKey(Story)

    # DocumentFile fields
    # (all handled via inline models)
    head = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    files = models.ManyToManyField("DocumentFile")

##    class Admin:
##        list_display        = ('name', 'created', 'head')
##        list_filter         = ('created',)
##        search_fields       = ('name', 'head', 'body')

    class Meta:
        verbose_name        = "Document"

    def __unicode__(self):
        return self.head


class DocumentFile(models.Model):
    file_obj = models.FileField("File", upload_to="stories/")
    name = models.CharField("Name of file", max_length=255)
    caption = models.CharField(max_length=255, blank=True, help_text="For giving \
        individual files separate captions. Optional.")

    class Admin:
        pass

    def __unicode__(self):
        return self.name
