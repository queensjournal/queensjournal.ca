import datetime
from django.db import models


class PublishedStoryManager(models.Manager):
    def get_query_set(self):
        return super(PublishedStoryManager, self).get_query_set().filter(
            pub_date__lt=datetime.datetime.now(), status='p')
