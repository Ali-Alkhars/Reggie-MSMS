from django.conf import settings
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from lessons.models import User
from lessons.management.commands.create_user_groups import Command
from lessons.tests.helpers import reverse_with_next

class AdminAccountsViewTestCase(TestCase):
    """Tests of the admin_accounts view."""

    fixtures = ['lessons/tests/fixtures/default_user.json']

    def setUp(self):
        create_groups_command = Command()
        create_groups_command.handle()

        self.url = reverse('admin_accounts')
        self.user = User.objects.get(username='johndoe@example.org')

    def test_admin_accounts_url(self):
        self.assertEqual(self.url,'/admin_accounts/')

    def test_get_admin_accounts(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        self._create_test_admins(10)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_accounts.html')
        self.assertEqual(len(response.context['admins']), 10)
        for user_id in range(10):
            self.assertContains(response, f'user{user_id}@test.org')
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')

    def test_post_admin_accounts_redirects_to_register_super_director(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        response = self.client.post(self.url, data={'user_type': 'director'})
        redirect_url = reverse('register_super', kwargs={'user_type': 'director'})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_admin_accounts_redirects_to_register_super_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        response = self.client.post(self.url, data={'user_type': 'admin'})
        redirect_url = reverse('register_super', kwargs={'user_type': 'admin'})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_admin_accounts_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_logged_in_director_can_access_admin_accounts_page(self):
        self.client.login(username = self.user.username, password = "Password123")
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        response = self.client.get(reverse('admin_accounts'))
        self.assertEqual(response.status_code, 200)

    def test_logged_out_director_cannot_access_admin_accounts_page(self):
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        response = self.client.get(reverse('admin_accounts'))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_student_cannot_access_admin_accounts_page(self):
        self.client.login(username = self.user.username, password = "Password123")
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(self.user)
        response = self.client.get(reverse('admin_accounts'))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_admin_cannot_access_admin_accounts_page(self):
        self.client.login(username = self.user.username, password = "Password123")
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(self.user)
        response = self.client.get(reverse('admin_accounts'))
        self.assertEqual(response.status_code, 302)

    def _create_test_admins(self, user_count=10):
        admin_group = Group.objects.get(name='admin') 
        for user_id in range(user_count):
            temp_user = User.objects.create_user(f'user{user_id}@test.org',
                password='Password123',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
            )
            admin_group.user_set.add(temp_user)

