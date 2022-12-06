"""Unit tests for the lesson request page."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from lessons.models import Lesson_request, User
from lessons.forms import LessonRequestForm
from lessons.management.commands.create_user_groups import Command
from lessons.tests.helpers import reverse_with_next
from django.conf import settings


class LessonRequestPageTestCase(TestCase):
    """Unit tests for the lesson request page"""

    fixtures = [
        'lessons/tests/fixtures/default_lesson_request.json',
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json'

    ]

    def setUp(self):
        create_groups_command = Command()
        create_groups_command.handle()
        self.url = reverse('lesson_request')
        # Can change to student foreign key when implemented
        self.lesson_request = Lesson_request.objects.get(AdditionalNotes= "I know how to play piano.")
        self.user = User.objects.get(username='peterpickles@example.org')
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(self.user)

    def test_lesson_request_url(self):
        self.assertEqual(self.url, '/lesson_page/lesson_request/')

    def test_lesson_request(self):
        self.client.login(username = self.user.username, password = 'Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lesson_request.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LessonRequestForm))
        self.assertFalse(form.is_bound)
    
    def test_redirect_when_user_access_lesson_request_not_loggedin(self):
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    
    def test_redirect_when_admin_access_lesson_request(self):
        user2 = User.objects.get(username='petrapickles@example.org')
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(user2)
        self.client.login(username=user2.username, password= 'Password123')
        response = self.client.get(self.url)
        redirect_url = reverse('home')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_redirect_when_director_access_lesson_request(self):
        user3 = User.objects.get(username='johndoe@example.org')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(user3)
        self.client.login(username=user3.username, password= 'Password123')
        response = self.client.get(self.url)
        redirect_url = reverse('home')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_lesson_request_with_blank_days(self):
        self.client.login(username = self.user.username, password = "Password123")
        form_input = {
            'availableDays': "", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        before_count = Lesson_request.objects.count()
        response = self.client.post(self.url, form_input, follow=True)
        after_count = Lesson_request.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lesson_request.html')

    def test_post_lesson_request_with_blank_times(self):
        self.client.login(username = self.user.username, password = "Password123")
        form_input = {
            'availableDays': "Monday", 
            'availableTimes': '',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        before_count = Lesson_request.objects.count()
        response = self.client.post(self.url, form_input, follow=True)
        after_count = Lesson_request.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
    
    def test_post_lesson_request_with_zero_lesson(self):
        self.client.login(username = self.user.username, password = "Password123")
        form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 0,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        before_count = Lesson_request.objects.count()
        response = self.client.post(self.url, form_input, follow=True)
        after_count = Lesson_request.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)

    def test_post_lesson_request_with_negative_number_of_lessons(self):
        self.client.login(username = self.user.username, password = "Password123")
        form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": -1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        before_count = Lesson_request.objects.count()
        response = self.client.post(self.url, form_input, follow=True)
        after_count = Lesson_request.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
    
    def test_post_lesson_request_with_zero_interval_between_lessons(self):
        self.client.login(username = self.user.username, password = "Password123")
        form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 0,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        before_count = Lesson_request.objects.count()
        response = self.client.post(self.url, form_input, follow=True)
        after_count = Lesson_request.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
    
    def test_post_lesson_request_with_negative_interval_between_lessons(self):
        self.client.login(username = self.user.username, password = "Password123")
        form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": -20,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        before_count = Lesson_request.objects.count()
        response = self.client.post(self.url, form_input, follow=True)
        after_count = Lesson_request.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
    
    def test_post_lesson_request_with_zero_duration_of_lessons(self):
        self.client.login(username = self.user.username, password = "Password123")
        form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 0,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        before_count = Lesson_request.objects.count()
        response = self.client.post(self.url, form_input, follow=True)
        after_count = Lesson_request.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
    
    def test_post_lesson_request_with_negative_interval_between_lessons(self):
        self.client.login(username = self.user.username, password = "Password123")
        form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": -30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        before_count = Lesson_request.objects.count()
        response = self.client.post(self.url, form_input, follow=True)
        after_count = Lesson_request.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)

    def test_successful_lesson_request(self):
        self.client.login(username = self.user.username, password = "Password123")
        form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        before_count = Lesson_request.objects.count()
        response = self.client.post(self.url, form_input, follow=True)
        after_count = Lesson_request.objects.count()
        self.assertEqual(after_count, before_count+1)
        redirect_url = reverse('lesson_page')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'lesson_page.html')
        # Can change to student foreign key when implemented
        lesson = Lesson_request.objects.get(AdditionalNotes="I know how to play violin")
        self.assertEqual(lesson.availableDays, 'Monday')
        self.assertEqual(lesson.availableTimes, 'Night')
        self.assertEqual(lesson.numberOfLessons, 1)
        self.assertEqual(lesson.IntervalBetweenLessons, 5)
        self.assertEqual(lesson.DurationOfLesson, 30)
        self.assertEqual(lesson.LearningObjectives, "I want to learn music.")
        self.assertEqual(lesson.AdditionalNotes, "I know how to play violin")





       

        