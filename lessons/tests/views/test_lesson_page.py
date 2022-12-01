"""Unit tests for the lesson showing page."""
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from lessons.models import Lesson_request, User
from lessons.forms import LessonRequestForm
from django.contrib.auth.models import Group
from lessons.management.commands.create_user_groups import Command
from lessons.tests.helpers import reverse_with_next
from django.conf import settings
from lessons.views import lesson_page, lesson_request
from django.contrib.sessions.middleware import SessionMiddleware
from importlib import import_module
from django.contrib.sessions.models import Session

# class modifySession(object):
#     client = Client()

#     def create_session(self):
#         sessionEngine = import_module(settings.SESSION_ENGINE)
#         store = sessionEngine.SessionStore()
#         store.save()
#         self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

class LessonPageTestCase(TestCase):
    """Unit tests for the lesson showing page"""
    fixtures = [
            'lessons/tests/fixtures/default_user.json',
            'lessons/tests/fixtures/other_users.json'
        ]
    
    def setUp(self):
        create_groups_command = Command()
        create_groups_command.handle()

        self.url = reverse('lesson_page')
        self.url2 = reverse('lesson_request')
        self.user = User.objects.get(username='peterpickles@example.org')
        self.user2 = User.objects.get(username='petrapickles@example.org')
        self.user3 = User.objects.get(username='johndoe@example.org')

        student_group = Group.objects.get(name='student')
        student_group.user_set.add(self.user)
        student_group.user_set.add(self.user2)

        self.admin = self.client.login(username=self.user3.username, password= 'Password123')
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(self.user3)

        self.form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }

    def test_lesson_page_url(self):
        self.assertEqual(self.url,'/lesson_page/')
    
    def test_get_lesson_page_redirects_when_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_user_logged_in_table_result(self):
        self.client.logout()
        self.client.login(username=self.user.username, password= 'Password123')
        response1 = self.client.post(self.url2, self.form_input, follow=True)
        self.client.login(username=self.user2.username, password= 'Password123')
        response2 = self.client.post(self.url2, self.form_input, follow=True)
        after_count = Lesson_request.objects.count()
        
        self.client.get(self.url)
        session = self.client.session
        self.assertEqual(session['countOfTable'], after_count-1)
    
    def test_admin_logged_in_table_result(self):
        response1 = self.client.post(self.url2, self.form_input, follow=True)
        response2 = self.client.post(self.url2, self.form_input, follow=True)
        response2 = self.client.post(self.url2, self.form_input, follow=True)
        after_count = Lesson_request.objects.count()

        self.client.get(self.url)
        session = self.client.session
        self.assertEqual(0, after_count)
        self.assertEqual(session['countOfTable'], after_count)

    def test_count_of_table_result_when_submit_lesson_form_with_empty_available_days(self):
        form_input2 = {
            'availableDays': "", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        self.client.login(username=self.user.username, password= 'Password123')
        response1 = self.client.post(self.url2, self.form_input, follow=True)
        response2 = self.client.post(self.url2, form_input2, follow=True)
        after_count = Lesson_request.objects.count()

        self.client.get(self.url)
        session = self.client.session
        self.assertEqual(1, after_count)
        self.assertEqual(session['countOfTable'], after_count)
    
    def test_count_of_table_result_when_submit_lesson_form_with_empty_available_times(self):
        form_input2 = {
            'availableDays': "Monday", 
            'availableTimes': '',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        self.client.login(username=self.user.username, password= 'Password123')
        response1 = self.client.post(self.url2, self.form_input, follow=True)
        response2 = self.client.post(self.url2, form_input2, follow=True)
        after_count = Lesson_request.objects.count()

        self.client.get(self.url)
        session = self.client.session
        self.assertEqual(1, after_count)
        self.assertEqual(session['countOfTable'], after_count)
    
    def test_count_of_table_result_when_submit_lesson_form_with_0_number_of_lessons(self):
        form_input2 = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 0,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        self.client.login(username=self.user.username, password= 'Password123')
        response1 = self.client.post(self.url2, self.form_input, follow=True)
        response2 = self.client.post(self.url2, form_input2, follow=True)
        after_count = Lesson_request.objects.count()

        self.client.get(self.url)
        session = self.client.session
        self.assertEqual(1, after_count)
        self.assertEqual(session['countOfTable'], after_count)
    
    def test_count_of_table_result_when_submit_lesson_form_with_negative_number_of_lessons(self):
        form_input2 = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": -1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        self.client.login(username=self.user.username, password= 'Password123')
        response1 = self.client.post(self.url2, self.form_input, follow=True)
        response2 = self.client.post(self.url2, form_input2, follow=True)
        after_count = Lesson_request.objects.count()

        self.client.get(self.url)
        session = self.client.session
        self.assertEqual(1, after_count)
        self.assertEqual(session['countOfTable'], after_count)
    
    def test_count_of_table_result_when_submit_lesson_form_with_0_interval_between_lessons(self):
        form_input2 = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 0,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        self.client.login(username=self.user.username, password= 'Password123')
        response1 = self.client.post(self.url2, self.form_input, follow=True)
        response2 = self.client.post(self.url2, form_input2, follow=True)
        after_count = Lesson_request.objects.count()

        self.client.get(self.url)
        session = self.client.session
        self.assertEqual(1, after_count)
        self.assertEqual(session['countOfTable'], after_count)
    
    def test_count_of_table_result_when_submit_lesson_form_with_negative_interval_between_lessons(self):
        form_input2 = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": -5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        self.client.login(username=self.user.username, password= 'Password123')
        response1 = self.client.post(self.url2, self.form_input, follow=True)
        response2 = self.client.post(self.url2, form_input2, follow=True)
        after_count = Lesson_request.objects.count()

        self.client.get(self.url)
        session = self.client.session
        self.assertEqual(1, after_count)
        self.assertEqual(session['countOfTable'], after_count)
    
    def test_count_of_table_result_when_submit_lesson_form_with_0_duration_of_lessons(self):
        form_input2 = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 0,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        self.client.login(username=self.user.username, password= 'Password123')
        response1 = self.client.post(self.url2, self.form_input, follow=True)
        response2 = self.client.post(self.url2, form_input2, follow=True)
        after_count = Lesson_request.objects.count()

        self.client.get(self.url)
        session = self.client.session
        self.assertEqual(1, after_count)
        self.assertEqual(session['countOfTable'], after_count)

    def test_count_of_table_result_when_submit_lesson_form_with_negative_duration_of_lessons(self):
        form_input2 = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": -30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        self.client.login(username=self.user.username, password= 'Password123')
        response1 = self.client.post(self.url2, self.form_input, follow=True)
        response2 = self.client.post(self.url2, form_input2, follow=True)
        after_count = Lesson_request.objects.count()

        self.client.get(self.url)
        session = self.client.session
        self.assertEqual(1, after_count)
        self.assertEqual(session['countOfTable'], after_count)
    
    def test_user_redirect_to_a_new_lesson_request(self):
        self.client.login(username=self.user2.username, password= 'Password123')
        response = self.client.post(self.url2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lesson_request.html')
    
    def test_not_logged_in_user_redirect_when_requesting_new_lesson_request(self):
        self.client.login(username=self.user2.username, password= 'Password123')
        self.client.logout()
        response = self.client.post(self.url2)
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.url2)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_admin_redirect_back_to_home_page_when_pushing_lesson_request_button(self):
        redirect_url = reverse('home')
        response = self.client.post(self.url2)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    
    def test_director_redirect_back_to_home_page_when_pushing_lesson_request_button(self):
        user4 = User.objects.get(username='janedoe@example.org')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(user4)
        loggedInuser4 = self.client.login(username=user4.username, password= 'Password123')
        response = self.client.get(self.url)
        redirect_url = reverse('home')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    




        