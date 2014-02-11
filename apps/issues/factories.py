import factory
from datetime import datetime, timedelta

from .models import Issue, Volume
from structure.factories import FlatPlanConfigFactory


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
