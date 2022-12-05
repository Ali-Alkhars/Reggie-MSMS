"""Unit tests for the lesson request update page."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Lesson_request, User
from django.contrib.auth.models import Group
from lessons.management.commands.create_user_groups import Command
from lessons.tests.helpers import reverse_with_next
from django.conf import settings
from lessons.forms import LessonRequestForm

class LessonPageUpdateTestCase(TestCase):
    """Unit tests for the lesson request update page"""
    fixtures = [
            'lessons/tests/fixtures/default_user.json',
            'lessons/tests/fixtures/other_users.json',
            'lessons/tests/fixtures/default_lesson_request.json',
        ]
    
    def setUp(self):
        create_groups_command = Command()
        create_groups_command.handle()

        self.form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin",
            "Fulfilled": "Pending"
        }
        
        self.url2 = reverse('lesson_request')
        self.lesson_request = Lesson_request.objects.get(AdditionalNotes= "I know how to play piano.")
        self.user = User.objects.get(username='peterpickles@example.org')
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(self.user)

        self.client.login(username=self.user.username, password= 'Password123')

        self.client.post(self.url2, self.form_input, follow=True)
        self.listUsed = Lesson_request.objects.filter(student=self.user)[0]
        self.url = reverse('lesson_request_delete', kwargs={'id': self.listUsed.id})
        
    def test_lesson_request_delete_url(self):
        self.assertEqual(self.url, '/lesson_page/{}/delete/'.format(self.listUsed.id))
    
    def test_redirect_when_user_access_lesson_request_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        
    def test_successful_delete(self):
        before_count = Lesson_request.objects.count()
        # response = self.client.get(self.url, follow=True)
        response = self.client.post(self.url, {})
        after_count = Lesson_request.objects.count()
        self.assertEqual(after_count, before_count-1)
    
    
