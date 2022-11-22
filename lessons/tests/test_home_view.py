from django.test import TestCase
from django.urls import reverse

class HomePageRedirectsTest(TestCase):

    def setUp(self):
        self.url=reverse('main')

    def test_main_url(self):
        self.assertEqual(self.url, '/')

    def test_get_main(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    def test_log_in_button_redirect(self):
        response = self.client.post(reverse('log_in'))
        self.assertEqual(response.status_code, 200)

    def test_sign_up_button_redirect(self):
        response = self.client.post(reverse('sign_up'))
        self.assertEqual(response.status_code, 200)
