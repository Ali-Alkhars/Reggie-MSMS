"""Unit tests for the term time showing page."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import User, TermTime
from django.contrib.auth.models import Group
from lessons.management.commands.create_user_groups import Command
from lessons.tests.helpers import reverse_with_next
from django.conf import settings
from lessons.forms import NewTermForm

class TermTimePageTestCase(TestCase):
    """Unit tests for the term time showing page"""
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
    
    def test_term_time_url(self):
        self.assertEqual(self.url,'/term_time/')
    
    def test_get_term_time_page_redirects_when_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    
    def test_user_logged_in_table_result(self):
        self.client.post(self.url2, self.form_input)
        form_input2 = {
            'startDate': '2023-03-02',
            'endDate': '2023-06-04',
            'termOrder': 'Second term'
        }
        self.client.login(username=self.user2.username, password= 'Password123')
        self.client.post(self.url2, form_input2)
        after_count = TermTime.objects.count()

        self.client.get(self.url)
        session = self.client.session

        self.assertEqual(session['countOfTermTime'], after_count)
    
    def test_count_of_table_result_when_submit_term_time_form_with_empty_startDate(self):
        self.form_input['startDate'] = ''
        form = NewTermForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        response = self.client.post(self.url2, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'term_create.html')
        counts = TermTime.objects.count()

        self.client.get(self.url)
        session = self.client.session
        self.assertEqual(session['countOfTermTime'], counts)
    
    def test_count_of_table_result_when_submit_term_time_form_with_empty_endDate(self):
        self.form_input['endDate'] = ''
        form = NewTermForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        response = self.client.post(self.url2, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'term_create.html')
        counts = TermTime.objects.count()

        self.client.get(self.url)
        session = self.client.session
        self.assertEqual(session['countOfTermTime'], counts)
    
    def test_count_of_table_result_when_submit_term_time_form_with_empty_termOrder(self):
        self.form_input['termOrder'] = ''
        form = NewTermForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        response = self.client.post(self.url2, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'term_create.html')
        counts = TermTime.objects.count()

        self.client.get(self.url)
        session = self.client.session
        self.assertEqual(session['countOfTermTime'], counts)
    
    def test_count_of_table_result_when_submit_term_time_form_with_invalid_start_end_date(self):
        self.form_input['startDate'] = '2022-08-30'
        self.form_input['endDate'] = '2022-07-30'
        form = NewTermForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        response = self.client.post(self.url2, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'term_create.html')
        counts = TermTime.objects.count()

        self.client.get(self.url)
        session = self.client.session
        self.assertEqual(session['countOfTermTime'], counts)
    
    def test_count_of_table_result_when_submit_term_time_form_with_less_than_90_days_start_end_date(self):
        self.form_input['startDate'] = '2022-08-30'
        self.form_input['endDate'] = '2022-08-31'
        form = NewTermForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        response = self.client.post(self.url2, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'term_create.html')
        counts = TermTime.objects.count()

        self.client.get(self.url)
        session = self.client.session
        self.assertEqual(session['countOfTermTime'], counts)
    

    
    

