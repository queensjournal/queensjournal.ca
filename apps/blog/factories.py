from datetime import datetime, timedelta
import factory

from authors.factories import AuthorFactory
from blog.models import BlogImage, Blog, Entry


class BlogImageFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = BlogImage

    slug = 'test-blog-image'
    image = 'test'


class BlogFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Blog

    title = 'Test Blog'
    slug = 'test-blog'
    teaser = 'teaser'
    description = 'description'
    active = True
    #image = factory.SubFactory(BlogImageFactory())
    order = factory.Sequence(lambda n: n)


class EntryFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Entry

    title = 'Test Post'
    slug = 'test-blog-post'
    author = factory.SubFactory(AuthorFactory)
    tags = 'test, blog, post'
    content = 'here is my test post content'
    is_published = True
    pub_date = factory.Sequence(lambda n: datetime.now() - \
        timedelta(weeks=(n)), type=int)
