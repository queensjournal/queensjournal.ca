import datetime
from django.db import models


class IssueManager(models.Manager):
    def published(self):
        return self.get_query_set().filter(
            is_published='PUB', pub_date__lte=datetime.datetime.now())

    def latest(self):
        return self.published().order_by('-pub_date')[0]

    def next(self, issue):
        if issue != self.published().latest():
            return self.published().filter(pub_date__gt=issue.pub_date).\
                order_by('pub_date')[0]
        else:
            return False

    def previous(self, issue):
        if self.get_query_set().filter(pub_date__lt=issue.pub_date).count() > 0:
            return self.published().filter(pub_date__lt=issue.pub_date).\
                order_by('-pub_date')[0]
        else:
            return False
