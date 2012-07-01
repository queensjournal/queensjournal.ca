from datetime import datetime, timedelta
import factory
from structure.factories import SectionFactory, IssueFactory
from stories.models import Story


class StoryFactory(factory.Factory):
    FACTORY_FOR = Story

    head = 'testing'
    deck = u'Editor-in-Chief says this will help detect issues earlier'
    slug = u'journal-implements-tests'
    issue = factory.SubFactory(IssueFactory)
    pub_date = factory.Sequence(lambda n: datetime.now() - \
        timedelta(weeks=(n)), type=int)
    section = factory.SubFactory(SectionFactory)
    status = 'p'
