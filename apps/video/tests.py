import os
import shutil
from django.test import TestCase
from apps.tests import SiteTestHelper
from django.conf import settings
from django.core.urlresolvers import reverse

class VideoTestHelper(object):

    def setup_video_tests(self):
        super(VideoTestHelper, self).setUp()
        test_image_source = os.path.join(settings.DJANGO_ROOT, 'tests/test.jpg')
        self.test_image_dest = 'test_data/test.jpg'
        shutil.copy(test_image_source, os.path.join(settings.MEDIA_ROOT, self.test_image_dest))

    def create_video(self, **kwargs):
        self.setup_video_tests()
        defaults = {
            'name': u'Test Video',
            'slug': 'video1',
            'pub_date': 
            'link': u'http://www.youtube.com/watch?v=xnxz3acXM6w',
            'caption': u'Get it pregnant!',
            'photographer': self.create_author(),
            'screenshot': self.test_image_dest,
            'is_published': True,
        }
        defaults.update(kwargs)
        obj, created = Video.objects.get_or_create(**defaults)
        return obj


class VideoTests(VideoTestHelper, SiteTestHelper, TestCase):

    def test_video_index(self):
        self.create_video()
        self.create_video(name="Test Video 2", slug="video-2")
        resp = self.client.get(reverse('video-index'))
        self.assertEqual(resp.status_code, 200)

    def test_video_detail(self):
        video = self.create_video()
        resp = self.client.get(video.get_absolute_url())
        self.assertEqual(resp.status_code, 200)
