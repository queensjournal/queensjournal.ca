import os
import shutil
import datetime

from django.test import TestCase
from django.conf import settings
from stories.models import Story
from structure.models import Volume, FlatPlanConfig, FlatPlanSection, FrontConfig, Issue, \
    Section, Author
from sidelinks.models import SidebarLinkset
from video.models import Video


class StoryTests(TestCase):

    def setUp(self):
        test_image_source = os.path.join(os.path.dirname(__file__), 'tests/test.jpg')
        test_image_dest = 'test_data/test.jpg'
        shutil.copy(test_image_source, os.path.join(settings.MEDIA_ROOT, test_image_dest))

        self.volume = Volume.objects.create(
            volume = 138
        )

        self.section = Section.objects.create(
            name = u'News',
            short_name = u'News',
            slug = 'news',
        )

        self.flatplanconfig = FlatPlanConfig.objects.create(
            name = u'Standard Issue'
        )

        self.flatplansection = FlatPlanSection.objects.create(
            section = self.section,
            config = self.flatplanconfig,
        )

        self.issue = Issue.objects.create(
            issue = 1,
            volume = self.volume,
            pub_date = datetime.date.today(),
            sections = self.flatplanconfig,
            is_published = 'PUB'
        )

        self.frontconfig = FrontConfig.objects.create(
            pub_date = datetime.datetime.today(),
            sections = self.flatplanconfig,
            issue = self.issue,
        )

        self.menulinks = SidebarLinkset.objects.create(
            name = u'Menu',
            slug = u'menu-sections',
        )

        self.main = SidebarLinkset.objects.create(
            name = u'Main',
            slug = u'main',
        )

        self.main2 = SidebarLinkset.objects.create(
            name = u'Main2',
            slug = u'main2',
        )

        self.author = Author.objects.create(
            name = u'Tracy Morgan',
            slug = u'tracy-morgan',
            email = u'tracymorgan@gmail.com',
        )

        self.story = Story.objects.create(
            head = u'Queen\'s Journal Implements testing framework, finally.',
            deck = u'Editor-in-Chief says this will help detect issues earlier',
            slug = u'journal-implements-tests',
            pub_date = datetime.datetime.now(),
            section = self.section,
        )

        self.video = Video.objects.create(
            name = u'Breaking Bad - S02E08',
            slug = u'video1',
            pub_date = datetime.datetime.now() - datetime.timedelta(weeks=1),
            link = u'http://www.youtube.com/watch?v=xnxz3acXM6w',
            caption = u'Get it pregnant!',
            photographer = self.author,
            screenshot = test_image_dest,
            is_published = True,
        )

    def test_index_front(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_story_detail(self):
        resp = self.client.get(self.story.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

    def tearDown(self):
        self.video.delete()
