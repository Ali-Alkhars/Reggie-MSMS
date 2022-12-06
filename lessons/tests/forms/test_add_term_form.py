"""Unit tests of the Add Term form."""
from lessons.forms import TermForm
from django.test import TestCase
from django import forms


class TermFormTestCase(TestCase):
    """Unit tests of the add term form."""

    def setUp(self):
        self.form_input = {'startDate': '2022-01-01', 'endDate': '2022-03-01'}

    def test_from_contains_required_fields(self):
        form = TermForm()
        self.assertIn('startDate', form.fields)
        self.assertIn('endDate', form.fields)
        startField = form.fields['startDate']
        endField = form.fields['endDate']
        self.assertTrue(isinstance(startField, forms.DateField))
        self.assertTrue(isinstance(endField, forms.DateField))

    def test_form_accepts_valid_input(self):
        form = TermForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_incorrect_startDate(self):
        self.form_input['startDate'] = 'Orange'
        form = TermForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_incorrect_endDate(self):
        self.form_input['endDate'] = 'Apple'
        form = TermForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_username(self):
        self.form_input['startDate'] = ''
        form = TermForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_password(self):
        self.form_input['endDate'] = ''
        form = TermForm(data=self.form_input)
        self.assertFalse(form.is_valid())
