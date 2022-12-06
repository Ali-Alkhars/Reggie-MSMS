from django.conf import settings
from lessons.forms import EditLoginsForm, EditPasswordForm
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from lessons.models import User
from lessons.tests.helpers import reverse_with_next
from django.contrib import messages

class EditAccountViewTestCase(TestCase):
    """Tests of the edit_account view."""

    fixtures = [
            'lessons/tests/fixtures/default_user.json',
            'lessons/tests/fixtures/other_users.json'
        ]

    def setUp(self):
        self.logins_form_input = {
            'first_name': 'John2',
            'last_name': 'Doe2',
            'username': 'johndoe2@example.org',
        }
        self.password_form_input = {
            'current_password': 'Password123',
            'new_password': 'NewPassword123',
            'confirm_password': 'NewPassword123',
        }
        self.url = reverse('edit_account', kwargs={'action': 'None'})
        self.user = User.objects.get(username='johndoe@example.org')

    def test_edit_account_url(self):
        self.assertEqual(self.url, '/edit_account/None')

    def test_get_edit_account(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_account.html')
        logins_form = response.context['logins_form']
        password_form = response.context['password_form']
        self.assertTrue(isinstance(logins_form, EditLoginsForm))
        self.assertTrue(isinstance(password_form, EditPasswordForm))
        self.assertEqual(logins_form.instance, self.user)

    def test_unsuccesful_logins_edit(self):
        self.client.login(username=self.user.username, password='Password123')
        self.logins_form_input['username'] = 'johndoe'
        before_count = User.objects.count()
        self.url = reverse('edit_account', kwargs={'action': 'logins'})
        response = self.client.post(self.url, self.logins_form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_account.html')
        logins_form = response.context['logins_form']
        self.assertTrue(isinstance(logins_form, EditLoginsForm))
        self.assertTrue(logins_form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'johndoe@example.org')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')

    def test_unsuccesful_logins_edit_due_to_duplicate_username(self):
        self.client.login(username=self.user.username, password='Password123')
        self.logins_form_input['username'] = 'janedoe@example.org'
        before_count = User.objects.count()
        self.url = reverse('edit_account', kwargs={'action': 'logins'})
        response = self.client.post(self.url, self.logins_form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_account.html')
        logins_form = response.context['logins_form']
        self.assertTrue(isinstance(logins_form, EditLoginsForm))
        self.assertTrue(logins_form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'johndoe@example.org')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')

    def test_succesful_logins_edit(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = User.objects.count()
        self.url = reverse('edit_account', kwargs={'action': 'logins'})
        response = self.client.post(self.url, self.logins_form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_account.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'johndoe2@example.org')
        self.assertEqual(self.user.first_name, 'John2')
        self.assertEqual(self.user.last_name, 'Doe2')

    def test_succesful_password_edit(self):
        self.client.login(username=self.user.username, password='Password123')
        self.url = reverse('edit_account', kwargs={'action': 'password'})
        response = self.client.post(self.url, self.password_form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_account.html')
        self.user.refresh_from_db()
        is_password_correct = check_password('NewPassword123', self.user.password)
        self.assertTrue(is_password_correct)

    def test_password_edit_unsuccesful_without_correct_previous_password(self):
        self.client.login(username=self.user.username, password='Password123')
        self.password_form_input['current_password'] = 'WrongPassword123'
        self.url = reverse('edit_account', kwargs={'action': 'password'})
        response = self.client.post(self.url, self.password_form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_account.html')
        form = response.context['password_form']
        self.assertTrue(isinstance(form, EditPasswordForm))
        self.user.refresh_from_db()
        is_password_correct = check_password('Password123', self.user.password)
        self.assertTrue(is_password_correct)

    def test_password_edit_unsuccesful_without_correct_confirm_password(self):
        self.client.login(username=self.user.username, password='Password123')
        self.password_form_input['confirm_password'] = 'WrongPassword123'
        self.url = reverse('edit_account', kwargs={'action': 'password'})
        response = self.client.post(self.url, self.password_form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_account.html')
        form = response.context['password_form']
        self.assertTrue(isinstance(form, EditPasswordForm))
        self.user.refresh_from_db()
        is_password_correct = check_password('Password123', self.user.password)
        self.assertTrue(is_password_correct)

    def test_user_is_redirected_to_home_if_no_action_given(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.post(self.url, self.password_form_input, follow=True)
        redirect_url = reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_edit_account_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_edit_account_password_redirects_when_not_logged_in(self):
        self.url = reverse('edit_account', kwargs={'action': 'password'})
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.url)
        response = self.client.post(self.url, self.password_form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        is_password_correct = check_password('Password123', self.user.password)
        self.assertTrue(is_password_correct)

    def test_post_edit_account_logins_redirects_when_not_logged_in(self):
        self.url = reverse('edit_account', kwargs={'action': 'logins'})
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.url)
        response = self.client.post(self.url, self.logins_form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)