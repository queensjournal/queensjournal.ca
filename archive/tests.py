from django.test import TestCase
from django.core.urlresolvers import reverse

from utils import SiteTestHelper
from issues.factories import IssueFactory, VolumeFactory


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

    def test_archive_volume_list(self):
        self.assert_page_loads(reverse('archive-volume-list'),
            'archives/volume_list.html')

    def test_archive_volume_detail(self):
        volume = self.volumes[0]
        self.assert_page_loads(reverse('archive-volume-detail',
            args=[volume.volume]), 'archives/volume_detail.html')

    def test_legacy_archive_issue_detail(self):
        issue = self.issues[0]
        resp = self.client.get(
            reverse('legacy-archive-issue-detail',
            args=[
                issue.pub_date.strftime('%Y'),
                issue.pub_date.strftime('%m'),
                issue.pub_date.strftime('%d'),
            ])
        )
        self.assertEqual(resp.status_code, 301)
