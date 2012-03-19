from django.test import TestCase
from django.core.urlresolvers import reverse

from apps.tests import SiteTestHelper


class ArchiveTests(SiteTestHelper, TestCase):
    def test_archive_index(self):
        self.create_frontconfig() # TODO remove this later
        resp = self.client.get(reverse('archive-index'))
        self.assertEqual(resp.status_code, 200)

    def test_archive_index_volume(self):
        self.create_frontconfig() # TODO remove this later
        volume = self.create_volume()
        resp = self.client.get(reverse('archive-volume-index',
            kwargs={ 'volume': volume.volume }))
        self.assertEqual(resp.status_code, 200)

