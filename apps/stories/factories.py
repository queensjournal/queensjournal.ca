import datetime
import factory
from structure.factories import SectionFactory, AuthorFactory
from stories.models import Story


class StoryFactory(factory.Factory):
    FACTORY_FOR = Story

    head = 'Queen\'s Journal Implements testing framework, finally.'
    deck = u'Editor-in-Chief says this will help detect issues earlier'
    slug = u'journal-implements-tests'
    pub_date = datetime.datetime.now()
    section = factory.SubFactory(SectionFactory)
