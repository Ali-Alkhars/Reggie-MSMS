"""Unit tests for the Term model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from lessons.models import Term

class LessonRequestModelTestCase(TestCase):
    """Unit tests for the Term model."""

    fixtures = [
        'lessons/tests/fixtures/default_term.json'
    ]

    def setUp(self):
        self.term = Term.objects.get(termID=1)

    def test_valid_term(self):
        self._assert_term_is_valid()

    def test_startDate_cannot_be_blank(self):
        self.term.startDate = ''
        self._assert_term_is_invalid()

    def test_endDate_cannot_be_blank(self):
        self.term.endDate = ''
        self._assert_term_is_invalid()




