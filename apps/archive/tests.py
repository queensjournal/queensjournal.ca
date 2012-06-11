from django.test import TestCase
from django.core.urlresolvers import reverse

from structure.factories import IssueFactory, VolumeFactory


class ArchiveTests(TestCase):
    def setUp(self):
        self.volumes = []
        self.issues = []

        for _ in range(3):
            self.volumes.append(VolumeFactory())

        for volume in self.volumes:
            for _ in range(2):
                self.issues.append(IssueFactory(volume=volume))

    def test_archive_index(self):
        resp = self.client.get(reverse('archive-index'))
        self.assertEqual(resp.status_code, 200)

    def test_archive_index_volume(self):
        volume = self.volumes[0]
        resp = self.client.get(reverse('archive-volume-index', args=[volume.volume]))
        self.assertEqual(resp.status_code, 200)
