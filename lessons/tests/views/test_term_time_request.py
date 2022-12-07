"""Unit tests for the term time request page."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import TermTime, User
from django.contrib.auth.models import Group
from lessons.management.commands.create_user_groups import Command
from lessons.tests.helpers import reverse_with_next
from django.conf import settings
from lessons.forms import NewTermForm

class TermTimeRequestTestCase(TestCase):
    """Unit tests for the term time request page"""
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
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(self.user2)
    
        self.form_input = {
            'startDate': '2022-08-30',
            'endDate': '2023-03-01',
            'termOrder': 'First term'
        }
        self.url = reverse('term_create')
    
    def test_term_time_request_url(self):
        self.assertEqual(self.url, '/term_time/term_create/')
    
    def test_redirect_when_user_access_term_time_request_not_logged_in(self):
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
    
    def test_redirect_when_admin_access_term_time_request(self):
        self.client.login(username=self.user2.username, password= 'Password123')
        response = self.client.get(self.url)
        redirect_url = reverse('home')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    
    def test_post_term_time_request_with_blank_startDate(self):
        self.form_input['startDate'] = ''
        before_count = TermTime.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = TermTime.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'term_create.html')
    
    def test_post_term_time_request_with_blank_endDate(self):
        self.form_input['endDate'] = ''
        before_count = TermTime.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = TermTime.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'term_create.html')
    
    def test_post_term_time_request_with_blank_termOrder(self):
        self.form_input['termOrder'] = ''
        before_count = TermTime.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = TermTime.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'term_create.html')
    
    def test_post_term_time_request_with_invalid_start_date_end_date(self):
        self.form_input['startDate'] = '2022-08-30'
        self.form_input['endDate'] = '2022-07-30'
        before_count = TermTime.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = TermTime.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'term_create.html')
    
    def test_post_term_time_request_with_less_than_90_days_start_end_date(self):
        self.form_input['startDate'] = '2022-08-30'
        self.form_input['endDate'] = '2022-09-30'
        before_count = TermTime.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = TermTime.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'term_create.html')
    

    
    
