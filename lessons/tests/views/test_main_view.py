from django.test import TestCase
from django.urls import reverse

class MainPageRedirectsTest(TestCase):

    def test_get_main(self):
        response = self.client.post(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    def test_log_in_button_redirect(self):
        response = self.client.post(reverse('log_in'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')


    def test_register_button_redirect(self):
        response = self.client.post(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register_as_student.html')
