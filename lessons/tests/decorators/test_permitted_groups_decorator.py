from django.test import TestCase
from lessons.models import User
from django.urls import reverse
from django.contrib.auth.models import Group
from django.conf import settings 
from lessons.management.commands.create_user_groups import Command

class PermittedGroupsTestCase(TestCase):
    """
    Unit tests for the @permitted_groups decorator
    This class assumes the following:
        - There is a page 'home' accessible by everyone
        - There is a page 'new_lesson' accessible only by students
        - There is a page 'lesson_requests' accessible only by admins or directors
    """

    fixtures = ['lessons/tests/fixtures/default_user.json']
    
    def setUp(self):
        create_groups_command = Command()
        create_groups_command.handle()
        self.user = User.objects.get(username= "johndoe@example.org")
        self.client.login(username = self.user.username, password = "Password123")

    def test_student_can_access_new_lesson_page(self):
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(self.user)

        response = self.client.get(reverse('new_lesson'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_can_access_lesson_requests_page(self):
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(self.user)

        response = self.client.get(reverse('lesson_requests'))
        self.assertEqual(response.status_code, 200)

    def test_director_can_access_lesson_requests_page(self):
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)

        response = self.client.get(reverse('lesson_requests'))
        self.assertEqual(response.status_code, 200)    

    # TODO: Add Templates assertions later when templates are implemented for all "cannot_access" tests

    def test_student_cannot_access_lesson_requests_page(self):
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(self.user)

        response = self.client.get(reverse('lesson_requests'), follow=True)
        redirect_url = reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_admin_cannot_access_new_lesson_page(self):
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(self.user)

        response = self.client.get(reverse('new_lesson'), follow=True)
        redirect_url = reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_director_cannot_access_new_lesson_page(self):
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)

        response = self.client.get(reverse('new_lesson'), follow=True)
        redirect_url = reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    