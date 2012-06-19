from django.test import TestCase
from django.core.urlresolvers import reverse

from utils import SiteTestHelper
from structure.factories import IssueFactory, VolumeFactory


class ArchiveTests(SiteTestHelper, TestCase):
    def setUp(self):
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
