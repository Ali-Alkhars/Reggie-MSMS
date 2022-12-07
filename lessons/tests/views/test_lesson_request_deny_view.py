from django.test import TestCase
from django.urls import reverse
from lessons.models import Invoice, Lesson_request, User
from django.contrib.auth.models import Group
from lessons.management.commands.create_user_groups import Command
from lessons.tests.helpers import reverse_with_next
from django.conf import settings

class LessonRequestDenyTestCase(TestCase):
    """Unit tests for the lesson request deny page"""
    fixtures = [
            'lessons/tests/fixtures/default_user.json',
            'lessons/tests/fixtures/other_users.json',
            'lessons/tests/fixtures/default_lesson_request.json',
        ]
    
    def setUp(self):
        create_groups_command = Command()
        create_groups_command.handle()
        self.user = User.objects.get(username='johndoe@example.org')
        self.student = User.objects.get(username= "janedoe@example.org")
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(self.student)
        self.lesson_request = Lesson_request.objects.get(AdditionalNotes= "I know how to play piano.")
        self.url = reverse('lesson_request_deny', kwargs={'id': self.lesson_request.id})

    def test_lesson_request_deny_url(self):
        self.assertEqual(self.url, f'/lesson_page/{self.lesson_request.id}/deny')

    def test_get_lesson_request_deny_as_director(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        count_lessons_before = len(Lesson_request.objects.all())
        self.assertEqual(self.lesson_request.Fulfilled, 'Pending')
        response = self.client.get(self.url, follow=True)
        self.lesson_request = Lesson_request.objects.get(id=self.lesson_request.id)
        count_lessons_after = len(Lesson_request.objects.all())
        self.assertEqual(count_lessons_before, count_lessons_after)
        self.assertEqual(self.lesson_request.Fulfilled, 'Denied')
        self.assertEqual(response.status_code, 200)
        redirect_url = reverse('lesson_page')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    
    def test_get_lesson_request_deny_as_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(self.user)
        count_lessons_before = len(Lesson_request.objects.all())
        self.assertEqual(self.lesson_request.Fulfilled, 'Pending')
        response = self.client.get(self.url, follow=True)
        self.lesson_request = Lesson_request.objects.get(id=self.lesson_request.id)
        count_lessons_after = len(Lesson_request.objects.all())
        self.assertEqual(count_lessons_before, count_lessons_after)
        self.assertEqual(self.lesson_request.Fulfilled, 'Denied')
        self.assertEqual(response.status_code, 200)
        redirect_url = reverse('lesson_page')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_lesson_request_deny_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_logged_in_student_cannot_access_lesson_request_deny(self):
        self.client.login(username = self.user.username, password = "Password123")
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)