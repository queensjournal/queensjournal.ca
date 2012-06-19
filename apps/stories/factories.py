from datetime import datetime, timedelta
import factory
from structure.factories import SectionFactory
from stories.models import Story


class StoryFactory(factory.Factory):
    FACTORY_FOR = Story

    head = 'Queen\'s Journal Implements testing framework, finally.'
    deck = u'Editor-in-Chief says this will help detect issues earlier'
    slug = u'journal-implements-tests'
    pub_date = factory.Sequence(lambda n: datetime.now() - \
        timedelta(weeks=(n)), type=int)
    section = factory.SubFactory(SectionFactory)
    status = 'p'
