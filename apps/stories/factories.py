from datetime import datetime, timedelta
import factory
from issues.factories import IssueFactory
from sections.factories import SectionFactory
from stories.models import Story


class StoryFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Story

    head = 'testing'
    deck = u'Editor-in-Chief says this will help detect issues earlier'
    slug = u'journal-implements-tests'
    issue = factory.SubFactory(IssueFactory)
    pub_date = factory.Sequence(lambda n: datetime.now() - \
        timedelta(weeks=(n)), type=int)
    section = factory.SubFactory(SectionFactory)
    status = 'p'
