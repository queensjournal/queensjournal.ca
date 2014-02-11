import factory

from .models import FlatPlanConfig


class FlatPlanConfigFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = FlatPlanConfig

    name = 'Test FlatPlan'
