import datetime
from django.test import TestCase
from stories.factories import StoryFactory

class StoryTests(TestCase):

    def setUp(self):
        self.story = StoryFactory()

    def test_story_detail(self):
        resp = self.client.get(self.story.get_absolute_url())
        self.assertEqual(resp.status_code, 200)
