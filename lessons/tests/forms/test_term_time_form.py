from django.test import TestCase
from lessons.forms import NewTermForm
from lessons.models import TermTime

class TermTimeFormTestCase(TestCase):
    """Unit tests of the term time form"""

    fixtures = ['lessons/tests/fixtures/default_user.json', 
                'lessons/tests/fixtures/default_term_time.json'
    ]

    def setUp(self):
        self.form_input = {
            'startDate': '2022-08-30',
            'endDate': '2023-03-01',
            'termOrder': 'First term'
        }
        object = TermTime.objects.all()[0]
        object.delete()
    
    def test_form_contains_required_fields(self):
        form = NewTermForm()
        self.assertIn('startDate', form.fields)
        self.assertIn('endDate', form.fields)
        self.assertIn('termOrder', form.fields)
    
    def test_form_accept_valid_input(self):

        form = NewTermForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_reject_blank_start_date(self):
        self.form_input['startDate'] = ''
        form = NewTermForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_reject_blank_end_date(self):
        self.form_input['endDate'] = ''
        form = NewTermForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_reject_blank_term_order(self):
        self.form_input['termOrder'] = ''
        form = NewTermForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_reject_when_end_date_larger_than_start_date(self):
        self.form_input['startDate'] = '2022-09-30'
        self.form_input['endDate'] = '2022-08-30'
        form = NewTermForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_reject_when_end_date_and_start_date_difference_are_less_than_90_days(self):
        self.form_input['startDate'] = '2022-08-30'
        self.form_input['endDate'] = '2022-09-30'
        form = NewTermForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    
    
    
