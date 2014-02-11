import factory

from .models import FlatPlanConfig


class FlatPlanConfigFactory(factory.Factory):
    FACTORY_FOR = FlatPlanConfig

    name = 'Test FlatPlan'
