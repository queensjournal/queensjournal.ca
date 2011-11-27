from django.db import models
from structure.models import Volume

class MastheadManager(models.Manager):
    def latest(self):
        return self.get_query_set().order_by('-volume')[0]


class Masthead(models.Model):
    volume = models.ForeignKey(Volume)
    objects = MastheadManager()

    class Admin:
        pass

    def __unicode__(self):
        return "Volume %s" % self.volume.volume


class MastheadName(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    section = models.ForeignKey('MastheadSection')
    individual_email = models.CharField(max_length=255, blank=True)
    masthead = models.ForeignKey(Masthead)

    class Meta:
        order_with_respect_to = 'masthead'

    def __unicode__(self):
        return "%s, %s" % (self.name, self.position)


class MastheadSection(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True)

    class Admin:
        pass

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.email)
