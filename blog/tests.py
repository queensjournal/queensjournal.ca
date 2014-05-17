from django.test import TestCase
from django.core.urlresolvers import reverse

from utils import SiteTestHelper
from blog.factories import BlogFactory, EntryFactory


class BlogTests(SiteTestHelper, TestCase):
    def setUp(self):
        super(BlogTests, self).setUp()
        self.blog = BlogFactory()
        self.entry = EntryFactory(blog=self.blog)

    def test_blog_list(self):
        self.assert_page_loads(reverse('all_blogs'),
            'blog/blog_list.html')

    def test_blog_index(self):
        self.assert_page_loads(reverse('blog-index', args=[self.blog.slug]),
            'blog/entry_list.html')

    def test_blog_detail(self):
        self.assert_page_loads(self.entry.get_absolute_url(),
            'blog/entry_detail.html')
