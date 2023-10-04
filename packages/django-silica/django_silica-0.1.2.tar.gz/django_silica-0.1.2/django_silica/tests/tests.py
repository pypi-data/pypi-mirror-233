# import json
#
# from django.core.cache import cache
# from django.test import TestCase, RequestFactory, Client
#
# from infabrica.components.TestComponent import TestComponent
#
#
# class InfabricaViewTestCase(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.client = Client()
#
#     def test_can_see_cached_property(self):
#         request = RequestFactory().get("/")
#
#         response = TestComponent.as_view()(request)
#         component_id = response.component.component_id
#
#         # Simulate an attribute stored in cache
#         cache.set(f"silica:component:{component_id}", {"first_name": "James"})
#
#         response = self.client.post(
#             "/infabrica/message",
#             json.dumps(
#                 {
#                     "id": component_id,
#                     "name": "infabrica.components.TestComponent.TestComponent",
#                 }
#             ),
#             content_type="application/json",
#         )
#
#         self.assertContains(response, "James")
#
#     def test_state_is_preserved_between_requests(self):
#         request = RequestFactory().get("/")
#
#         response = TestComponent.as_view()(request)
#         component_id = response.component.component_id
#
#         # Simulate an attribute stored in cache
#         cache.set(f"silica:component:{component_id}", {"first_name": "James"})
#
#         # Simulate a /message request
#         response = self.client.post(
#             "/infabrica/message",
#             json.dumps(
#                 {
#                     "id": component_id,
#                     "name": "infabrica.components.TestComponent.TestComponent",
#                 }
#             ),
#             content_type="application/json",
#         )
#
#         self.assertContains(response, "James")
#
#         # A subsequent request to /message should return the same state
#         response = self.client.post(
#             "/infabrica/message",
#             json.dumps(
#                 {
#                     "id": component_id,
#                     "name": "infabrica.components.TestComponent.TestComponent",
#                 }
#             ),
#             content_type="application/json",
#         )
#
#         self.assertContains(response, "James")
