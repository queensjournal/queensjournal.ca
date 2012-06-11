from config.factories import SiteConfigFactory
from structure.factories import IssueFactory


class SiteTestHelper(object):
    '''
    Global test helper that provides a SiteConfig and base issue for global
    tests
    '''
    def setUp(self):
        super(SiteTestHelper, self).setUp()
        SiteConfigFactory()
        IssueFactory()
