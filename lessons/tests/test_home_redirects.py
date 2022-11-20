from django.test import TestCase
from django.urls import reverse

class HomePageRedirectsTest(TestCase):

    def setUp(self):
        self.url=reverse('home')

    def test_log_in_button_redirect(self):
        response = self.client.post(reverse('log_in'))
        self.assertEqual(response.status_code, 200)

    def test_sign_up_button_redirect(self):
        response = self.client.post(reverse('sign_up'))
        self.assertEqual(response.status_code, 200)
