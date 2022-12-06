"""Unit tests for the lesson request update page."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Lesson_request, User
from django.contrib.auth.models import Group
from lessons.management.commands.create_user_groups import Command
from lessons.tests.helpers import reverse_with_next
from django.conf import settings
from lessons.forms import LessonRequestForm

class TermTimeUpdateTestCase(TestCase):
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
        self.url = reverse('lesson_request_update', kwargs={'id': self.listUsed.id})
        
    
    def test_lesson_request_update_url(self):
        self.assertEqual(self.url, '/lesson_page/{}/update/'.format(self.listUsed.id))
    
    def test_redirect_when_user_access_lesson_request_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    
    def test_lesson_request_update(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(isinstance(form, LessonRequestForm))
        self.assertFalse(form.is_bound)
    
    def test_post_lesson_request_update_no_change_with_different_types_of_fulfilled(self):
        form_input = {
            'availableDays': "", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin",
            "Fulfilled": "Approved"
        }

        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        lesson = Lesson_request.objects.filter(student=self.user)[0]
        self.assertEqual(lesson.Fulfilled, "Pending")
    

    def test_post_lesson_request_update_with_blank_days(self):
        form_input = {
            'availableDays': "", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin",
            "Fulfilled": "Pending"
        }

        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        lesson = Lesson_request.objects.filter(student=self.user)[0]
        self.assertEqual(lesson.availableDays, "Monday")
    
    def test_post_lesson_request_update_with_blank_times(self):
        form_input = {
            'availableDays': "Monday", 
            'availableTimes': '',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin",
            "Fulfilled": "Pending"
        }

        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        lesson = Lesson_request.objects.filter(student=self.user)[0]
        self.assertEqual(lesson.availableTimes, "Night")
    
    def test_post_lesson_request_update_with_zero_number_of_lessons(self):
        form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 0,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin",
            "Fulfilled": "Pending"
        }

        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        lesson = Lesson_request.objects.filter(student=self.user)[0]
        self.assertEqual(lesson.numberOfLessons, 1)
    
    def test_post_lesson_request_update_with_negative_number_of_lessons(self):
        form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": -20,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin",
            "Fulfilled": "Pending"
        }

        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        lesson = Lesson_request.objects.filter(student=self.user)[0]
        self.assertEqual(lesson.numberOfLessons, 1)
    
    def test_post_lesson_request_update_with_zero_interval_between_lessons(self):
        form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 0,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin",
            "Fulfilled": "Pending"
        }

        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        lesson = Lesson_request.objects.filter(student=self.user)[0]
        self.assertEqual(lesson.IntervalBetweenLessons, 5)
    
    def test_post_lesson_request_update_with_negative_interval_between_lessons(self):
        form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": -20,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin",
            "Fulfilled": "Pending"
        }

        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        lesson = Lesson_request.objects.filter(student=self.user)[0]
        self.assertEqual(lesson.IntervalBetweenLessons, 5)
    
    def test_post_lesson_request_update_with_zero_duration_of_lessons(self):
        form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 0,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin",
            "Fulfilled": "Pending"
        }

        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        lesson = Lesson_request.objects.filter(student=self.user)[0]
        self.assertEqual(lesson.DurationOfLesson, 30)
    
    def test_post_lesson_request_update_with_negative_duration_of_lessons(self):
        form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": -20,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin",
            "Fulfilled": "Pending"
        }

        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        lesson = Lesson_request.objects.filter(student=self.user)[0]
        self.assertEqual(lesson.DurationOfLesson, 30)
    
    def test_post_lesson_request_update_with_empty_learning_objectives(self):
        form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "",
            "AdditionalNotes": "I know how to play violin",
            "Fulfilled": "Pending"
        }

        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        lesson = Lesson_request.objects.filter(student=self.user)[0]
        self.assertEqual(lesson.LearningObjectives, "I want to learn music.")
    
    def test_post_lesson_request_update_successful_with_empty_additional_notes(self):
        form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I love piano",
            "Fulfilled": "Pending"
        }

        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        lesson = Lesson_request.objects.filter(student=self.user)[0]
        self.assertEqual(lesson.AdditionalNotes, "I love piano")
    
    

    
    
    





    

    
    
