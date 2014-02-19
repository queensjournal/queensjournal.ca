import datetime
from django.db import models
from config.models import SiteConfig


class VideoManager(models.Manager):
    def published(self):
        return self.get_query_set().filter(
            is_published=True, pub_date__lt=datetime.datetime.now()
        )

    def latest(self):
        return self.published().first()

    def featured(self):
        config = SiteConfig.get()
        if not config.featured_video:
            return self.published()[:1].get()
        return config.featured_video
