import factory
from config.models import SiteConfig


class SiteConfigFactory(factory.Factory):
    FACTORY_FOR = SiteConfig

    featured_tags = 'test, test2, test3'
