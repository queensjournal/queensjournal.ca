import factory

from .models import Section


class SectionFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Section

    name = factory.Sequence(lambda n: "Test Section %s" % n)
    short_name = factory.Sequence(lambda n: "Test %s" % n)
    slug = factory.Sequence(lambda n: "test-%s" % n)
