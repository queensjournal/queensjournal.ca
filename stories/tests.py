from django.test import TestCase

from utils import SiteTestHelper
from stories.models import Story
from stories.factories import StoryFactory
from stories.managers import StoryManager


class StoryTests(SiteTestHelper, TestCase):
    def setUp(self):
        self.story = StoryFactory()

    def test_story_detail(self):
        self.assert_page_loads(self.story.get_absolute_url(),
            'stories/story_detail.html')

    def test_story_returns_404_if_unpublished(self):
        story = StoryFactory(status='d')
        resp = self.client.get(story.get_absolute_url())
        self.assertEqual(resp.status_code, 404)

class StoryManagerTests(TestCase):
    def test_publised_manager_does_not_include_unpublished_stories(self):
        unpublished = StoryFactory(status='d')
        published = StoryFactory(status='p')
        stories = Story.objects.published()
        self.assertTrue(published in stories)
        self.assertFalse(unpublished in stories)
