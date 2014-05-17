from django.test import TestCase
from django.core.urlresolvers import reverse

from utils import SiteTestHelper


class TagsViewsTests(SiteTestHelper, TestCase):
    def test_tag_cloud(self):
        self.assert_page_loads(reverse('tag-index'))
