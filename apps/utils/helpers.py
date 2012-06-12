from django.db.models.query import QuerySet

from config.factories import SiteConfigFactory
from structure.factories import IssueFactory


class SiteTestHelper(object):
    '''
    Global test helper that provides a SiteConfig and base issue for global
    tests
    '''
    def setUp(self):
        SiteConfigFactory()
        IssueFactory()

    def assert_page_loads(self, url, template_name=None, context=None):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        if template_name is not None:
            self.assertTemplateUsed(response, template_name)

        if context is not None:
            for k, v in context.iteritems():
                self.assertIn(k, response.context)

                if isinstance(v, QuerySet):     # convert QuerySets into lists for comparison
                    v = list(v)                 # as QuerySet has no eq operator.

                response_value = response.context[k]
                if isinstance(response_value, QuerySet):
                    response_value = list(response_value)

                self.assertEqual(v, response_value)
