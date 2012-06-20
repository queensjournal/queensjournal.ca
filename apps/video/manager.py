import datetime
from django.db import models


class PublishedVideoManager(models.Manager):
    def get_query_set(self):
        return super(PublishedVideoManager, self).get_query_set().filter(
            pub_date__lt=datetime.datetime.now(), status='p')
