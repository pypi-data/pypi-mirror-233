from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser

from silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest
from silica.tests.components.QueryParams import QueryParams


class QueryParamTests(SilicaTestCase):
    def test_query_params_can_be_set(self):
        (
            SilicaTest(component=QueryParams)
            .assertSet("property_1", "foo")
            .assertSee("foo")
        )

        request = RequestFactory().get("/?property_1=bar")
        request.user = AnonymousUser()

        (
            SilicaTest(component=QueryParams, request=request)
            .assertSet("property_1", "bar")
            .assertSee("bar")
        )

        # response = self.client.get("/test?first_name=James")
        #
        # self.assertContains(response, "James")

    def test_properties_set_query_params(self):
        response = self.client.get("/test")

        self.assertContains(response, "Smith")
