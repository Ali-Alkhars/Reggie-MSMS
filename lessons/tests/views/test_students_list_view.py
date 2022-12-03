from django.conf import settings
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from lessons.models import User
from lessons.management.commands.create_user_groups import Command
from lessons.tests.helpers import reverse_with_next

class StudentsListViewTestCase(TestCase):
    """Tests of the students_list view."""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        create_groups_command = Command()
        create_groups_command.handle()
        self.user = User.objects.get(username= "johndoe@example.org")
        self.url = reverse('students_list')

    def test_students_list_url(self):
        self.assertEqual(self.url, f'/students_list/')

    def test_get_students_list_as_director(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        self._add_students()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students_list.html')
        self.assertEqual(len(response.context['users']), 2)
        self.assertContains(response, 'janedoe@example.org')
        self.assertContains(response, 'peterpickles@example.org')

    def test_get_students_list_as_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(self.user)
        self._add_students()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students_list.html')
        self.assertEqual(len(response.context['users']), 2)
        self.assertContains(response, 'janedoe@example.org')
        self.assertContains(response, 'peterpickles@example.org')

    def test_get_students_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_logged_in_student_cannot_access_students_list_page(self):
        self.client.login(username = self.user.username, password = "Password123")
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def _add_students(self):
        self.jane = User.objects.get(username= "janedoe@example.org")
        self.peter = User.objects.get(username= "peterpickles@example.org")
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(self.jane)
        student_group.user_set.add(self.peter)