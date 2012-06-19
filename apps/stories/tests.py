from django.test import TestCase

from utils import SiteTestHelper
from stories.factories import StoryFactory


class StoryTests(SiteTestHelper, TestCase):
    def setUp(self):
        self.story = StoryFactory()

    def test_story_detail(self):
        self.assert_page_loads(self.story.get_absolute_url(),
            'stories/single_detail.html')
