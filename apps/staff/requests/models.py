import datetime, random, re, hashlib
from django.db import models
from django.conf import settings
from django.core.mail import send_mail, mail_managers
from django.contrib.auth.models import User
from django.template import Context, loader
from structure.models import Section

class RequestsManager(models.Manager):
    def unassigned(self):
        return self.get_query_set().filter(status='UNA').order_by('-time')

    def unreceived(self):
        return self.get_query_set().filter(models.Q(status='UNA') | models.Q(status='ASS')).order_by('-time')
    

class PhotoRequest(models.Model):
    # available to requesters
    subject = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    time = models.DateTimeField("Time of shoot", blank=True, null=True)
    creator = models.ForeignKey(User)
    section = models.ForeignKey(Section)
    deadline = models.DateField()
    notes = models.TextField(blank=True)

    STATUS_OPTIONS = (
        ('0', 'Unassigned'),
        ('1', 'Assigned'),
        ('2', 'Photos received'),
        ('3', 'Ready for layout')
    )
    # available to photo editors
    status = models.CharField(max_length=1, choices=STATUS_OPTIONS, default="0")
    photographer = models.CharField(max_length=255, blank=True)

    # added/changed date fields
    added = models.DateTimeField(default=datetime.datetime.now)
    changed = models.DateTimeField(default=datetime.datetime.now)

    # objects manager
    objects = RequestsManager()

    def urgent(self):
        """
        Helper function for templates. Warns if the photo shoot
        or deadline is within two days. (The value of two days is
        hardcoded because Django's template language can't do basic
        arithmetic. High-larious.)
        """
        if self.time is not None:
            delta = self.time - datetime.datetime.now()
        else:
            delta = self.deadline - datetime.date.today()
        return delta.days <= 2 and self.status == "0"

    class Admin:
        list_display    = ('subject', 'location', 'time', 'status', 'section', 'deadline')
        list_filter     = ('time', 'status', 'section', 'deadline')

    class Meta:
        ordering        = ('-deadline', 'status', '-time', 'section')
        permissions     = (("view_photorequest", "Can view photo request"),)

    def get_absolute_url(self):
        return "/staff/requests/view/%i" % self.id
