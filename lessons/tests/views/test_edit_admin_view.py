from django.conf import settings
from django.contrib.auth.models import Group
from lessons.forms import EditLoginsForm, EditPasswordForm
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from lessons.models import User
from lessons.management.commands.create_user_groups import Command
from lessons.tests.helpers import reverse_with_next
from django.contrib import messages

class EditAdminViewTestCase(TestCase):
    """Tests of the edit_admin view."""

    fixtures = [
            'lessons/tests/fixtures/default_user.json',
            'lessons/tests/fixtures/other_users.json'
        ]

    def setUp(self):
        create_groups_command = Command()
        create_groups_command.handle()

        self.peter = User.objects.get(username='peterpickles@example.org')
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(self.peter)

        self.logins_form_input = {
            'first_name': 'Peter2',
            'last_name': 'Pickles2',
            'username': 'peterpickles2@example.org',
        }
        self.password_form_input = {
            'current_password': 'Password123',
            'new_password': 'NewPassword123',
            'confirm_password': 'NewPassword123',
        }
        self.action = 'None'
        self.url = reverse('edit_admin', kwargs={'action': self.action, 'user_id': self.peter.id})
        self.user = User.objects.get(username='johndoe@example.org')

    def test_edit_admin_url(self):
        self.assertEqual(self.url, f'/edit_admin/{self.action}/{self.peter.id}')

    def test_get_edit_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_admin.html')
        logins_form = response.context['logins_form']
        password_form = response.context['password_form']
        self.assertTrue(isinstance(logins_form, EditLoginsForm))
        self.assertTrue(isinstance(password_form, EditPasswordForm))
        self.assertEqual(logins_form.instance, self.peter)

    def test_unsuccesful_logins_edit(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        self.logins_form_input['username'] = 'peterpickles'
        before_count = User.objects.count()
        self.action = 'logins'
        self.url = reverse('edit_admin', kwargs={'action': self.action, 'user_id': self.peter.id})
        response = self.client.post(self.url, self.logins_form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_admin.html')
        logins_form = response.context['logins_form']
        self.assertTrue(isinstance(logins_form, EditLoginsForm))
        self.assertTrue(logins_form.is_bound)
        self.peter.refresh_from_db()
        self.assertEqual(self.peter.username, 'peterpickles@example.org')
        self.assertEqual(self.peter.first_name, 'Peter')
        self.assertEqual(self.peter.last_name, 'Pickles')

    def test_unsuccesful_logins_edit_due_to_duplicate_username(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        self.logins_form_input['username'] = 'petrapickles@example.org'
        before_count = User.objects.count()
        self.action = 'logins'
        self.url = reverse('edit_admin', kwargs={'action': self.action, 'user_id': self.peter.id})
        response = self.client.post(self.url, self.logins_form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_admin.html')
        logins_form = response.context['logins_form']
        self.assertTrue(isinstance(logins_form, EditLoginsForm))
        self.assertTrue(logins_form.is_bound)
        self.peter.refresh_from_db()
        self.assertEqual(self.peter.username, 'peterpickles@example.org')
        self.assertEqual(self.peter.first_name, 'Peter')
        self.assertEqual(self.peter.last_name, 'Pickles')

    def test_succesful_logins_edit(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        before_count = User.objects.count()
        self.action = 'logins'
        self.url = reverse('edit_admin', kwargs={'action': self.action, 'user_id': self.peter.id})
        response = self.client.post(self.url, self.logins_form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_admin.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.peter.refresh_from_db()
        self.assertEqual(self.peter.username, 'peterpickles2@example.org')
        self.assertEqual(self.peter.first_name, 'Peter2')
        self.assertEqual(self.peter.last_name, 'Pickles2')

    def test_succesful_password_edit(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        self.action = 'password'
        self.url = reverse('edit_admin', kwargs={'action': self.action, 'user_id': self.peter.id})
        response = self.client.post(self.url, self.password_form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_admin.html')
        self.peter.refresh_from_db()
        is_password_correct = check_password('NewPassword123', self.peter.password)
        self.assertTrue(is_password_correct)

    def test_password_edit_unsuccesful_without_correct_previous_password(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        self.password_form_input['current_password'] = 'WrongPassword123'
        self.action = 'password'
        self.url = reverse('edit_admin', kwargs={'action': self.action, 'user_id': self.peter.id})
        response = self.client.post(self.url, self.password_form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_admin.html')
        form = response.context['password_form']
        self.assertTrue(isinstance(form, EditPasswordForm))
        self.peter.refresh_from_db()
        is_password_correct = check_password('Password123', self.peter.password)
        self.assertTrue(is_password_correct)

    def test_password_edit_unsuccesful_without_correct_confirm_password(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        self.password_form_input['confirm_password'] = 'WrongPassword123'
        self.action = 'password'
        self.url = reverse('edit_admin', kwargs={'action': self.action, 'user_id': self.peter.id})
        response = self.client.post(self.url, self.password_form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_admin.html')
        form = response.context['password_form']
        self.assertTrue(isinstance(form, EditPasswordForm))
        self.peter.refresh_from_db()
        is_password_correct = check_password('Password123', self.peter.password)
        self.assertTrue(is_password_correct)

    def test_user_is_redirected_to_admin_accounts_if_no_action_given(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        response = self.client.post(self.url, self.password_form_input, follow=True)
        redirect_url = reverse('admin_accounts')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_edit_admin_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_edit_admin_password_redirects_when_not_logged_in(self):
        self.url = reverse('edit_admin', kwargs={'action': 'password', 'user_id': self.peter.id})
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.url)
        response = self.client.post(self.url, self.password_form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        is_password_correct = check_password('Password123', self.user.password)
        self.assertTrue(is_password_correct)

    def test_post_edit_admin_logins_redirects_when_not_logged_in(self):
        self.url = reverse('edit_admin', kwargs={'action': 'logins', 'user_id': self.peter.id})
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.url)
        response = self.client.post(self.url, self.logins_form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_logged_out_director_cannot_access_edit_admin(self):
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_logged_in_student_cannot_access_edit_admin(self):
        self.client.login(username = self.user.username, password = "Password123")
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_logged_in_admin_cannot_access_edit_admin(self):
        self.client.login(username = self.user.username, password = "Password123")
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

