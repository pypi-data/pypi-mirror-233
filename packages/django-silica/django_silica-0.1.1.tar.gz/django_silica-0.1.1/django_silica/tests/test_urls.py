from django.test import TestCase, RequestFactory, Client

class TestUrls(TestCase):

    def setUp(self):
        self.client = Client()

    def test_dashboard_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)