import factory

from .models import Author


class AuthorFactory(factory.Factory):
    FACTORY_FOR = Author

    name = factory.Sequence(lambda n: "Test Author %s" % n)
    slug = factory.Sequence(lambda n: "test-author-%s" % n)
