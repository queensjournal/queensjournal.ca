from django.test import TestCase
from django.core.urlresolvers import reverse

from utils import SiteTestHelper
from .factories import IssueFactory


class IssueTests(SiteTestHelper, TestCase):
    def setUp(self):
        super(IssueTests, self).setUp()
        self.issue = IssueFactory()

    def test_issue_detail(self):
        self.assert_page_loads(
            reverse('issue-detail', args=[self.issue.volume.volume,
                self.issue.issue]),
            'archives/issue_detail.html')
