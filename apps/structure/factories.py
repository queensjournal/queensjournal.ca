import factory
from datetime import datetime, timedelta

from structure.models import Section, Author, Issue, Volume, FlatPlanConfig


class SectionFactory(factory.Factory):
    FACTORY_FOR = Section

    name = factory.Sequence(lambda n: "Test Section %s" % n)
    short_name = factory.Sequence(lambda n: "Test %s" % n)
    slug = factory.Sequence(lambda n: "test-%s" % n)


class AuthorFactory(factory.Factory):
    FACTORY_FOR = Author

    name = factory.Sequence(lambda n: "Test Author %s" % n)
    slug = factory.Sequence(lambda n: "test-author-%s" % n)


class FlatPlanConfigFactory(factory.Factory):
    FACTORY_FOR = FlatPlanConfig

    name = 'Test FlatPlan'


class VolumeFactory(factory.Factory):
    FACTORY_FOR = Volume

    volume = factory.Sequence(lambda n: n)


class IssueFactory(factory.Factory):
    FACTORY_FOR = Issue

    issue = factory.Sequence(lambda n: n)
    volume = factory.SubFactory(VolumeFactory)
    pub_date = factory.Sequence(lambda n: datetime.now() - \
        timedelta(weeks=n), type=int)
    sections = factory.SubFactory(FlatPlanConfigFactory)
    is_published = 'PUB'
