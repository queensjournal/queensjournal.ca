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
            delta = self.deadline - datetime.date.now()
        return delta.days <= 2 and self.status == "0"

    class Admin:
        list_display    = ('subject', 'location', 'time', 'status', 'section', 'deadline')
        list_filter     = ('time', 'status', 'section', 'deadline')

    class Meta:
        ordering        = ('-deadline', 'status', '-time', 'section')
        permissions     = (("view_photorequest", "Can view photo request"),)

    def get_absolute_url(self):
        return "/staff/requests/view/%i" % self.id


##class RequestUsersManager(models.Manager):
##    def create_user(self, username, password, email, first="", last="", role="RE"):
##        """
##        Creates a new PhotoRequestUser, handles registration details
##        and creates a new User. Role defaults to Requester;
##        anyone with change permissions on PhotoRequestUser (usually
##        just the webmaster) can change the role of a user.
##        """
##        # Create a User object.
##        user = User.objects.create_user(username, email, password)
##        user.is_active = False
##        if first and last:
##            user.first_name = first
##            user.last_name = last
##        user.save()
##
##        # Generate a salted SHA1 hash to use as a key.
##        salt = sha.new(str(random.random())).hexdigest()[:5]
##        activation_key = sha.new(salt+user.username).hexdigest()
##
##        # Create PhotoRequestUser.
##        new_req_user = self.create(user=user, role=role, activation_key=activation_key)
##
##        # send moderation e-mail to webmaster
##        subject = "Journal photo request board user activation"
##        message_template = loader.get_template('requests/activation_email.txt')
##        message_context = Context({ 'first_name': first,
##                                    'last_name': last,
##                                    'email': email,
##                                    'key': activation_key})
##        message = message_template.render(message_context)
##        mail_managers(subject, message)
##
##        # send notification e-mail to applicant
##        app_subject = "Your request for access to the Journal request board has been sent"
##        app_message_template = loader.get_template('requests/app_notification_email.txt')
##        app_message_context = Context({ 'username': username,
##                                        'first_name': first,
##                                        'last_name': last})
##        app_message = app_message_template.render(app_message_context)
##        send_mail(app_subject, app_message, settings.DEFAULT_FROM_EMAIL, [user.email])
##        return user
##
##    def activate_user(self, activation_key):
##        """
##        Grants a user access to the photo request board after moderation.
##        """
##        if re.match('[a-f0-9]{40}', activation_key):
##            try:
##                user_profile = self.get(activation_key=activation_key)
##            except self.model.DoesNotExist:
##                return False
##            user = user_profile.user
##            user.is_active=True
##            user.save()
##            # send a success e-mail to the user
##            app_subject = "Your request for access to the Journal request board has been granted"
##            app_message_template = loader.get_template('requests/app_success_email.txt')
##            app_message_context = Context({ 'username': user.username,
##                                            'first_name': user.first_name,
##                                            'last_name': user.last_name})
##            app_message = app_message_template.render(app_message_context)
##            send_mail(app_subject, app_message, settings.DEFAULT_FROM_EMAIL, [user.email])
##            return user
##        return False
##        
##    def editors(self):
##        """
##        Returns a list of all photo editors.
##        """
##        return self.get_query_set().filter(role="ED")
##
##    def requesters(self):
##        """
##        Returns a list of all requesters.
##        """
##        return self.get_query_set().filter(role="RE")
##    
##
##class PhotoRequestUser(models.Model):
##    # Choices for roles in the request system. Photographers could
##    # be added too, if desired.
##    ROLES = (
##        ('RE', 'Requester'),
##        ('ED', 'Photo Editor'),
##    )
##    user = models.ForeignKey(User, unique=True)
##    role = models.CharField(max_length=2, choices=ROLES)
##    activation_key = models.CharField(max_length=40)
##    objects = RequestUsersManager()
##    
##    class Admin:
##        pass
##    
