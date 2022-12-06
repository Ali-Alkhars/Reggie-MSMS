"""Unit tests for the term time update page."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import TermTime, User
from django.contrib.auth.models import Group
from lessons.management.commands.create_user_groups import Command
from lessons.tests.helpers import reverse_with_next
from django.conf import settings
from lessons.forms import NewTermForm
import datetime

class LessonPageUpdateTestCase(TestCase):
    """Unit tests for the term time update page"""
    fixtures = [
            'lessons/tests/fixtures/default_user.json',
            'lessons/tests/fixtures/other_users.json',
            'lessons/tests/fixtures/default_term_time.json',
            
        ]
    
    def setUp(self):
        create_groups_command = Command()
        create_groups_command.handle()

        self.user = User.objects.get(username='peterpickles@example.org')
        self.client.login(username=self.user.username, password= 'Password123')
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(self.user)

        self.user2 = User.objects.get(username='petrapickles@example.org')
        admin_group.user_set.add(self.user2)
    
        self.form_input = {
            'startDate': '2022-08-30',
            'endDate': '2023-03-01',
            'termOrder': 'First term'
        }
        self.url = reverse('term_time')
        self.url2 = reverse('term_create')

        self.client.post(self.url2, self.form_input, follow=True)
        self.listUsed = TermTime.objects.filter(startDate='2022-08-30')[0]
        self.url = reverse('term_time_update', kwargs={'id': self.listUsed.id})
    
    def test_lesson_request_update_url(self):
        self.assertEqual(self.url, '/term_time/{}/update/'.format(self.listUsed.id))
    
    def test_redirect_when_user_access_lesson_request_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    
    def test_term_time_update(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(isinstance(form, NewTermForm))
        self.assertFalse(form.is_bound)
    
    def test_post_lesson_request_update_no_change_with_empty_startDate(self):
        self.form_input['startDate'] = ''
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        term = TermTime.objects.filter(endDate='2023-03-01')[0]
        self.assertEqual(term.startDate, datetime.date(2022, 8, 30))
    
    def test_post_lesson_request_update_no_change_with_invalid_startDate(self):
        self.form_input['startDate'] = 'Hello'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        term = TermTime.objects.filter(endDate='2023-03-01')[0]
        self.assertEqual(term.startDate, datetime.date(2022, 8, 30))

    def test_post_lesson_request_update_no_change_with_empty_endDate(self):
        self.form_input['endDate'] = ''
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        term = TermTime.objects.filter(startDate='2022-08-30')[0]
        self.assertEqual(term.endDate, datetime.date(2023,3,1))
    
    def test_post_lesson_request_update_no_change_with_invalid_endDate(self):
        self.form_input['endDate'] = 'Hello'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        term = TermTime.objects.filter(startDate='2022-08-30')[0]
        self.assertEqual(term.endDate, datetime.date(2023,3,1))
    
    def test_post_lesson_request_update_no_change_with_empty_termOrder(self):
        self.form_input['termOrder'] = ''
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        term = TermTime.objects.filter(startDate='2022-08-30')[0]
        self.assertEqual(term.termOrder, 'First term')
    
    def test_post_lesson_request_update_no_change_with_invalid_end_date_start_date(self):
        self.form_input['endDate'] = '2022-09-30'
        self.form_input['startDate'] = '2022-10-30'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        term = TermTime.objects.filter(startDate = '2022-08-30')[0]
        self.assertEqual(term.startDate, datetime.date(2022,8,30))
        self.assertEqual(term.endDate, datetime.date(2023,3,1))
    
    def test_post_lesson_request_update_no_change_with_end_date_start_date_less_than_90_days(self):
        self.form_input['endDate'] = '2022-09-30'
        self.form_input['startDate'] = '2022-08-31'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        term = TermTime.objects.filter(startDate = '2022-08-30')[0]
        self.assertEqual(term.startDate, datetime.date(2022,8,30))
        self.assertEqual(term.endDate, datetime.date(2023,3,1))
    

    

    

    

        