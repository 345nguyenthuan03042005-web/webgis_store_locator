from django.test import TestCase


class SmokeTests(TestCase):
    def test_home_page_ok(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_map_page_ok(self):
        response = self.client.get('/map/')
        self.assertEqual(response.status_code, 200)

    def test_ping_api_ok(self):
        response = self.client.get('/tools/ping/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'ok': True, 'message': 'pong', 'pong': True})
