import datetime
from django.db import models


class StoryManager(models.Manager):
    def published(self):
        return self.get_query_set().filter(
                pub_date__lt=datetime.datetime.now(), status='p'
            )

    def latest(self):
        return self.published().latest()
