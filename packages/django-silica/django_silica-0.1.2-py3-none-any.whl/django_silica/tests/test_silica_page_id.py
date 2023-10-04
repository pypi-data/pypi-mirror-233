import json

from django.core.cache import cache
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, Client, TestCase
from django.http import HttpResponse

from django_silica.middleware import AddSilicaPageIdToRequest
from django_silica.tests.SilicaTestCase import SilicaTestCase
from django_silica.tests.components.Ops import Ops


class TestSilicaRequestPageId(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = AddSilicaPageIdToRequest(self.get_response)

    def get_response(self, request):
        return HttpResponse()

    def apply_middleware(self, request):
        # You can simulate a request through middleware like this.
        middleware = AddSilicaPageIdToRequest(lambda req: req)
        middleware(request)
        return request

    def test_middleware_adds_page_id(self):
        request = self.factory.get('/')

        # You can simulate a request through middleware like this.
        request = self.apply_middleware(request)

        # Ensure PAGE is not in the request META
        self.assertIn("_silicia_page_session_id", request.META)


    def test_middleware_doesnt_change_already_set_page_id(self):
        request = self.factory.get('/')
        request = self.apply_middleware(request)

        initial_page_session_id = request.META['_silicia_page_session_id']

        new_request = self.factory.get('/')
        new_request.META['_silicia_page_session_id'] = initial_page_session_id

        new_request = self.apply_middleware(new_request)
        new_request_page_session_id = new_request.META['_silicia_page_session_id']

        assert initial_page_session_id == new_request_page_session_id

    def test_component_carries_the_page_session_id_through_requests(self):
        pass