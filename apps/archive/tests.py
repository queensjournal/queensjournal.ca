from django.test import TestCase
from django.core.urlresolvers import reverse

from utils import SiteTestHelper
from structure.factories import IssueFactory, VolumeFactory, SectionFactory


class ArchiveTests(SiteTestHelper, TestCase):
    def setUp(self):
        super(ArchiveTests, self).setUp()
        self.volumes = []
        self.issues = []

        for _ in range(3):
            self.volumes.append(VolumeFactory())

        for volume in self.volumes:
            for _ in range(2):
                self.issues.append(IssueFactory(volume=volume))

    def test_archive_index(self):
        self.assert_page_loads(reverse('archive-index'), 'archives/index.html')

    def test_archive_index_volume(self):
        volume = self.volumes[0]
        self.assert_page_loads(reverse('archive-volume-index',
            args=[volume.volume]), 'archives/index_volume.html')

    def test_archive_issue_index(self):
        issue = self.issues[0]
        self.assert_page_loads(reverse('archive-issue-index',
            args=[issue.pub_date.date()]), 'archives/issue_detail.html')

    def test_archive_section_index(self):
        issue = self.issues[0]
        # TODO: this needs to test a section part of the original issue, else
        # return 404
        section = SectionFactory()
        self.assert_page_loads(reverse('archive-section-index',
            args=[issue.pub_date.date(), section.slug]),
            'archives/index_section.html')
