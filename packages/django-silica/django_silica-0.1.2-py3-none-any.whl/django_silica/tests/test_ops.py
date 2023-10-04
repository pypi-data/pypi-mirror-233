import json

from django.core.cache import cache
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, Client

from django_silica.tests.SilicaTestCase import SilicaTestCase
from django_silica.tests.components.Ops import Ops

class TestOps(SilicaTestCase):
    def setUp(self):
        self.client = Client()

    def test_can_see_cached_property(self):
        request = RequestFactory().get("/")
        request.user = AnonymousUser()

        response = Ops.as_view()(request)
        component_id = response.component.component_id

        # Simulate an attribute stored in cache
        cache.set(f"silica:component:{component_id}", {"first_name": "James"})

        response = self.client.post(
            "/silica/message",
            json.dumps(
                {
                    "id": component_id,
                    "name": "silica.tests.components.TestComponent.TestComponent",
                }
            ),
            content_type="application/json",
        )

        self.assertContains(response, "James")

    def test_state_is_preserved_between_requests(self):
        request = RequestFactory().get("/")
        request.user = AnonymousUser()

        response = Ops.as_view()(request)
        component_id = response.component.component_id

        # Simulate an attribute stored in cache
        cache.set(f"silica:component:{component_id}", {"first_name": "James"})

        # Simulate a /message request
        response = self.client.post(
            "/silica/message",
            json.dumps(
                {
                    "id": component_id,
                    "name": "silica.tests.components.TestComponent.TestComponent",
                }
            ),
            content_type="application/json",
        )

        self.assertContains(response, "James")

        # A subsequent request to /message should return the same state
        response = self.client.post(
            "/silica/message",
            json.dumps(
                {
                    "id": component_id,
                    "name": "silica.tests.components.TestComponent.TestComponent",
                }
            ),
            content_type="application/json",
        )

        self.assertContains(response, "James")
