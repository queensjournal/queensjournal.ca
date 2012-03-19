import datetime
from django.test import TestCase

from structure.models import Volume, Section, FlatPlanConfig, FlatPlanSection, \
    FrontConfig, Issue, Author
from sidelinks.models import SidebarLinkset


class SiteTestHelper(object):
    def create_volume(self, **kwargs):
        volume_num = Volume.objects.count() + 1
        defaults = {
            'volume' : volume_num
        }
        defaults.update(kwargs)
        return Volume.objects.create(**defaults)

    def create_section(self):
        return Section.objects.get_or_create(
            name       = u'News',
            short_name = u'News',
            slug       = 'news',
        )[0]

    def create_flatplansection(self):
        return FlatPlanSection.objects.get_or_create(
            section = self.create_section(),
            config = self.create_flatplanconfig(),
        )[0]

    def create_flatplanconfig(self, **kwargs):
        return FlatPlanConfig.objects.get_or_create(
            name = u'Standard Issue'
        )[0]

    def create_issue(self, **kwargs):
        issue_num = Issue.objects.count() + 1
        defaults = {
            'issue'        : issue_num,
            'volume'       : self.create_volume(),
            'pub_date'     : datetime.date.today(),
            'sections'     : self.create_flatplanconfig(),
            'is_published' : 'PUB'
        }
        defaults.update(kwargs)
        return Issue.objects.create(**defaults)

    def create_frontconfig(self, **kwargs):
        defaults = {
            'pub_date' : datetime.datetime.today(),
            'sections' : self.create_flatplanconfig(),
            'issue'    : self.create_issue(),
        }
        defaults.update(kwargs)
        return FrontConfig.objects.create(**defaults)

    def test_create_menulinks(self, **kwargs):
        self.menulinks = SidebarLinkset.objects.get_or_create(
            name = u'Menu',
            slug = u'menu-sections',
        )[0]

        self.main = SidebarLinkset.objects.get_or_create(
            name = u'Main',
            slug = u'main',
        )[0]

        self.main2 = SidebarLinkset.objects.get_or_create(
            name = u'Main2',
            slug = u'main2',
        )[0]
        return self.menulinks, self.main, self.main2

    AUTHOR_DEFAULTS = {
        'name': u'Tracy Morgan',
        'slug': u'tracy-morgan',
        'email': u'tracymorgan@gmail.com',
    }

    def create_author(self, **kwargs):
        defaults = self.AUTHOR_DEFAULTS.copy()
        defaults.update(**kwargs)
        obj, created = Author.objects.get_or_create(**defaults)
        return obj
