"""Unit tests for the Term time model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from lessons.models import TermTime

class TermTimeModelTestCase(TestCase):
    """Unit tests for the Term time model."""

    fixtures = [
        'lessons/tests/fixtures/default_term_time.json'
    ]

    def setUp(self):
        self.term_time = TermTime.objects.get(startDate = "2022-09-30")
    
    def test_valid_term_time_request(self):
        self._assert_term_time_is_valid()

    def test_startDate_cannot_be_blank(self):
        self.term_time.startDate = ''
        self._assert_term_time_is_invalid()
    
    def test_endDate_cannot_be_blank(self):
        self.term_time.endDate = ''
        self._assert_term_time_is_invalid()
    
    def test_midTerm_cannot_be_blank(self):
        self.term_time.midTerm = ''
        self._assert_term_time_is_invalid()
    
    def test_termOrder_cannot_be_blank(self):
        self.term_time.termOrder = ''
        self._assert_term_time_is_invalid()
    
    def _assert_term_time_is_valid(self):
        try:
            self.term_time.full_clean()
        except (ValidationError):
            self.fail('Test lesson request should be valid')

    def _assert_term_time_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.term_time.full_clean()


