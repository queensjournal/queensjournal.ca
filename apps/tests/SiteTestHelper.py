import datetime
from structure.models import Volume, Section, FlatPlanConfig, FlatPlanSection, \
    FrontConfig, Issue, Author
from sidelinks.models import SidebarLinkset


class SiteTestHelper(object):
    def create_volume(self, **kwargs):
        obj, created = Volume.objects.get_or_create(
            volume = 138
        )
        return obj

    def create_section(self):
        obj, created = Section.objects.get_or_create(
            name = u'News',
            short_name = u'News',
            slug = 'news',
        )
        return obj

    def create_flatplan(self, **kwargs):
        self.flatplanconfig = FlatPlanConfig.objects.get_or_create(
            name = u'Standard Issue'
        )[0]
        self.flatplansection = FlatPlanSection.objects.get_or_create(
            section = self.create_section(),
            config = self.flatplanconfig,
        )[0]
        return self.flatplanconfig

    def create_issue(self, **kwargs):
        obj, created = Issue.objects.get_or_create(
            issue = 1,
            volume = self.create_volume(),
            pub_date = datetime.date.today(),
            sections = self.create_flatplan(),
            is_published = 'PUB'
        )
        return obj

    def create_frontconfig(self, **kwargs):
        obj, created = FrontConfig.objects.get_or_create(
            pub_date = datetime.datetime.today(),
            sections = self.create_flatplan(),
            issue = self.create_issue(),
        )
        return obj

    def create_menulinks(self, **kwargs):
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
