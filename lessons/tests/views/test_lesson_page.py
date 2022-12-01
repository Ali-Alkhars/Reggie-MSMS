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
        # self.loggedinUser2 = self.client.login(username=self.user2.username, password= 'Password123')
        self.admin = self.client.login(username=self.user3.username, password= 'Password123')
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(self.admin)
        self.factory = RequestFactory()

    def test_lesson_page_url(self):
        self.assertEqual(self.url,'/lesson_page/')
    
    def test_get_lesson_page_redirects_when_not_logged_in(self):
        redirect_url = reverse("home")
        request = self.factory.get(self.url)
        request.user = self.user
        response = lesson_page(request)
        response.client = Client()
        self.assertRedirects(response, redirect_url, target_status_code=302)

    def test_user_logged_in_table_result(self):
        form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        form_input2 = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }

        # client = Client()
        # loggedinUser2 = client.login(username=self.user.username, password='Password123')
        # student_group = Group.objects.get(name='student')
        # student_group.user_set.add(loggedinUser2)
        # print(client)


        self.client.logout()
        # print(1)
        self.client.login(username=self.user.username, password= 'Password123')
        student_group = Group.objects.get(name='student')
        student_group.user_set.add(self.user)
        print(self.client)
        response1 = self.client.post(self.url2, form_input, follow=True)
        response2 = self.client.post(self.url2, form_input2, follow=True)
        after_count = Lesson_request.objects.count()
        # print(2)
        
        self.client.get(self.url)
        session = self.client.session

        # print(3)
        # request = self.factory.get(self.url)
        # request.user = self.loggedinUser2
        # middleware = SessionMiddleware(request)
        # middleware.process_request(request)
        # request.session.save()

        
        # client.get(self.url.format(self.user2.id), follow=True)
        # session = self.client.session
        self.assertEqual(session['countOfTable'], after_count)
    
    def test_admin_logged_in_table_result(self):
        form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        form_input2 = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }

        # self.client.force_login(self.user)
        response1 = self.client.post(self.url2, form_input, follow=True)
        response2 = self.client.post(self.url2, form_input2, follow=True)
        response2 = self.client.post(self.url2, form_input2, follow=True)
        after_count = Lesson_request.objects.count()

        self.client.get(self.url)
        session = self.client.session
        # request = self.factory.get(self.url)
        # request.user = self.admin
        # session = request.session.session_key
        print(session['countOfTable'])
        self.assertEqual(session['countOfTable'], after_count)
    


    
    # def test_user_redirect_to_a_new_lesson_request(self):




        