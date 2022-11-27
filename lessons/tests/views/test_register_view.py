from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from lessons.forms import RegisterForm
from lessons.models import User
from lessons.tests.helpers import LogInTester
from lessons.management.commands.create_user_groups import Command

class RegisterViewTestCase(TestCase, LogInTester):
    """Tests of the register view."""

    fixtures = ['lessons/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('register')
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': 'janedoe@example.org',
            'new_password': 'Password123',
            'confirm_password': 'Password123'
        }
        self.user = User.objects.get(username='johndoe@example.org')

    def test_register_url(self):
        self.assertEqual(self.url,'/register/')

    def test_get_register(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register_as_student.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RegisterForm))
        self.assertFalse(form.is_bound)

    def test_get_register_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')

    def test_unsuccessful_register(self):
        self.form_input['username'] = 'BAD_USERNAME'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register_as_student.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RegisterForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_successful_register(self):
        create_groups_command = Command()
        create_groups_command.handle()

        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        user = User.objects.get(username='janedoe@example.org')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        is_password_correct = check_password('Password123', user.password)
        self.assertEqual(user.groups.all()[0].name, 'student')
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())

    def test_post_register_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        redirect_url = reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
