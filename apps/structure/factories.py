import factory
from structure.models import Section, Author


class SectionFactory(factory.Factory):
    FACTORY_FOR = Section

    name = factory.Sequence(lambda n: "Test Section %s" % n)
    short_name = factory.Sequence(lambda n: "Test %s" % n)
    slug = factory.Sequence(lambda n: "test-%s" % n)

class AuthorFactory(factory.Factory):
    FACTORY_FOR = Author

    name = factory.Sequence(lambda n: "Test Author %s" % n)
    slug = factory.Sequence(lambda n: "test-author-%s" % n)
