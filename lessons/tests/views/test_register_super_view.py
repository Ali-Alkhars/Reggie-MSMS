from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from lessons.forms import RegisterForm
from lessons.models import User
from lessons.tests.helpers import LogInTester, reverse_with_next
from lessons.management.commands.create_user_groups import Command


class RegisterViewTestCase(TestCase, LogInTester):
    """Tests of the register_super view."""

    fixtures = ['lessons/tests/fixtures/default_user.json']

    def setUp(self):
        create_groups_command = Command()
        create_groups_command.handle()
        self.director_url = reverse('register_super', kwargs={'user_type': 'director'})
        self.admin_url = reverse('register_super', kwargs={'user_type': 'admin'})
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': 'janedoe@example.org',
            'new_password': 'Password123',
            'confirm_password': 'Password123'
        }
        self.user = User.objects.get(username='johndoe@example.org')

    def test_register_super_director_url(self):
        self.assertEqual(self.director_url,'/register_super/director')

    def test_register_super_admin_url(self):
        self.assertEqual(self.admin_url,'/register_super/admin')

    def test_get_register_super_director(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        response = self.client.get(self.director_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register_as_director.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RegisterForm))
        self.assertFalse(form.is_bound)

    def test_get_register_super_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register_as_admin.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RegisterForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_register_super_director(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        self.form_input['username'] = 'BAD_USERNAME'
        before_count = User.objects.count()
        response = self.client.post(self.director_url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register_as_director.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RegisterForm))
        self.assertTrue(form.is_bound)

    def test_unsuccessful_register_super_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        self.form_input['username'] = 'BAD_USERNAME'
        before_count = User.objects.count()
        response = self.client.post(self.admin_url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register_as_admin.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RegisterForm))
        self.assertTrue(form.is_bound)

    def test_successful_register_super_director(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        before_count = User.objects.count()
        response = self.client.post(self.director_url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse("admin_accounts")
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'admin_accounts.html')
        user = User.objects.get(username='janedoe@example.org')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        is_password_correct = check_password('Password123', user.password)
        self.assertEqual(user.groups.all()[0].name, 'director')
        self.assertTrue(is_password_correct)

    def test_successful_register_super_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        before_count = User.objects.count()
        response = self.client.post(self.admin_url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse("admin_accounts")
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'admin_accounts.html')
        user = User.objects.get(username='janedoe@example.org')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        is_password_correct = check_password('Password123', user.password)
        self.assertEqual(user.groups.all()[0].name, 'admin')
        self.assertTrue(is_password_correct)

    def test_get_register_super_director_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.director_url)
        response = self.client.get(self.director_url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_register_super_admin_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.admin_url)
        response = self.client.get(self.admin_url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_logged_out_director_cannot_access_register_super_director(self):
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        response = self.client.get(self.director_url)
        self.assertEqual(response.status_code, 302)

    def test_logged_in_student_cannot_access_register_super_director(self):
        self.client.login(username = self.user.username, password = "Password123")
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(self.user)
        response = self.client.get(self.director_url)
        self.assertEqual(response.status_code, 302)

    def test_logged_in_admin_cannot_access_register_super_director(self):
        self.client.login(username = self.user.username, password = "Password123")
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(self.user)
        response = self.client.get(self.director_url)
        self.assertEqual(response.status_code, 302)

    def test_logged_out_director_cannot_access_register_super_admin(self):
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, 302)

    def test_logged_in_student_cannot_access_register_super_admin(self):
        self.client.login(username = self.user.username, password = "Password123")
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(self.user)
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, 302)

    def test_logged_in_admin_cannot_access_register_super_admin(self):
        self.client.login(username = self.user.username, password = "Password123")
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(self.user)
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, 302)