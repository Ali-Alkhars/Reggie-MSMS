from django.conf import settings
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from lessons.models import User
from lessons.management.commands.create_user_groups import Command
from lessons.tests.helpers import reverse_with_next
from lessons.helpers.helper_functions import get_user_group_from_id

class AdminActionsViewTestCase(TestCase):
    """Tests of the admin_actions view."""

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

        self.action = 'None'
        self.url = reverse('admin_actions', kwargs={'action': self.action, 'user_id': self.peter.id})
        self.user = User.objects.get(username='johndoe@example.org')

    def test_admin_actions_url(self):
        self.assertEqual(self.url, f'/admin_actions/{self.action}/{self.peter.id}')

    def test_promote_action_promotes_admin_to_director(self):
        self.client.login(username = self.user.username, password = "Password123")
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        self.assertEqual('admin', get_user_group_from_id(self.peter.id))
        promotion_url = reverse('admin_actions', kwargs={'action': 'promote', 'user_id': self.peter.id})
        response = self.client.get(promotion_url, follow=True)
        self.assertEqual('director', get_user_group_from_id(self.peter.id))
        redirect_url = reverse('admin_accounts')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'admin_accounts.html')

    def test_edit_action_redirects_to_edit_admin(self):
        self.client.login(username = self.user.username, password = "Password123")
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        edit_url = reverse('admin_actions', kwargs={'action': 'edit', 'user_id': self.peter.id})
        response = self.client.get(edit_url, follow=True)
        redirect_url = reverse('edit_admin', kwargs={'action': 'None', 'user_id': self.peter.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'edit_admin.html')

    def test_delete_action_deletes_admin_user(self):
        self.client.login(username = self.user.username, password = "Password123")
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        before_user_count = len(User.objects.all())
        before_admins_count = len(User.objects.filter(groups__name='admin'))
        delete_url = reverse('admin_actions', kwargs={'action': 'delete', 'user_id': self.peter.id})
        response = self.client.get(delete_url, follow=True)
        self.assertEqual(len(User.objects.all()), before_user_count-1)
        self.assertEqual(len(User.objects.filter(groups__name='admin')), before_admins_count-1)
        redirect_url = reverse('admin_accounts')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'admin_accounts.html')

    def test_None_action_redirects_to_admin_accounts(self):
        self.client.login(username = self.user.username, password = "Password123")
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        edit_url = reverse('admin_actions', kwargs={'action': 'None', 'user_id': self.peter.id})
        response = self.client.get(edit_url, follow=True)
        redirect_url = reverse('admin_accounts')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'admin_accounts.html')

    def test_get_admin_actions_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_logged_out_director_cannot_make_admin_actions(self):
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_logged_in_student_cannot_make_admin_actions(self):
        self.client.login(username = self.user.username, password = "Password123")
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_logged_in_admin_cannot_make_admin_actions(self):
        self.client.login(username = self.user.username, password = "Password123")
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)