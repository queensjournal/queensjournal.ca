from django.db.models.query import QuerySet

from config.factories import SiteConfigFactory
from structure.factories import IssueFactory


class SiteTestHelper(object):
    '''
    Global test helper that provides a SiteConfig and base issue for global
    tests
    '''
    def setUp(self):
        self.config = SiteConfigFactory()
        self.issue = IssueFactory()

    def assert_page_loads(self, url, template_name=None, context=None):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        kwargs = {}

        if template_name is not None:
            kwargs['template_name'] = template_name
            self.assertTemplateUsed(response, template_name)

        if context is not None:
            kwargs['context'] = context
            for k, v in context.iteritems():
                self.assertIn(k, response.context)

                if isinstance(v, QuerySet):     # convert QuerySets into lists for comparison
                    v = list(v)                 # as QuerySet has no eq operator.

                response_value = response.context[k]
                if isinstance(response_value, QuerySet):
                    response_value = list(response_value)

                self.assertEqual(v, response_value)

        self.assert_mobile_page_loads(url, *kwargs)

    def assert_mobile_page_loads(self, url, template_name=None, context=None):
        response = self.client.get(url + '?flavour=mobile')
        self.assertEqual(response.status_code, 200)
