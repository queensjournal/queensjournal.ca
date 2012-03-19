import datetime
from django.test import TestCase
from video.tests import VideoTestHelper
from apps.tests import SiteTestHelper
from stories.models import Story

class StoryTests(SiteTestHelper, VideoTestHelper, TestCase):

    def create_story(self, **kwargs):
        defaults = {
            'head'     : u'Queen\'s Journal Implements testing framework, finally.',
            'deck'     : u'Editor-in-Chief says this will help detect issues earlier',
            'slug'     : u'journal-implements-tests',
            'pub_date' : datetime.datetime.now(),
            'section'  : self.create_section(),
        }
        defaults.update(kwargs)
        return Story.objects.create(**defaults)

    def test_index_front(self):
        self.create_video()
        self.create_video(name="Test Video 2", slug="video-2")
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_story_detail(self):
        story = self.create_story()
        resp = self.client.get(story.get_absolute_url())
        self.assertEqual(resp.status_code, 200)
