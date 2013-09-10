from django.test import TestCase

from utils import SiteTestHelper
from utils.factories import UserFactory
from stories.factories import StoryFactory


class PreviewTests(SiteTestHelper, TestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True)
        self.story = StoryFactory(status='d')

    def test_story_returns_when_user_is_staff(self):
        resp = self.client.get(self.story.get_absolute_url())
        self.assertEquals(resp.status_code, 200)

    def test_story_returns_404(self):
        self.user.is_staff = False
        resp = self.client.get(self.story.get_absolute_url())
        self.assertEquals(resp.status_code, 404)
