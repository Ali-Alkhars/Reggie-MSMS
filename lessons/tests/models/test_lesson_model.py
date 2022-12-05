"""Unit tests for the Lesson_request model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from lessons.models import Lesson_request

class LessonRequestModelTestCase(TestCase):
    """Unit tests for the Lesson_request model."""

    fixtures = [
        'lessons/tests/fixtures/default_lesson_request.json'
    ]

    def setUp(self):
        self.lesson_request = Lesson_request.objects.get(AdditionalNotes= "I know how to play piano.")

    def test_valid_lesson_request(self):
        self._assert_lesson_request_is_valid()
    
    def test_availableDays_cannot_be_blank(self):
        self.lesson_request.availableDays = ''
        self._assert_lesson_request_is_invalid()

    def test_availableDays_cannot_be_random_words(self):
        self.lesson_request.availableDays = 'vjiweog'
        self._assert_lesson_request_is_invalid()

    def test_availableTimes_cannot_be_blank(self):
        self.lesson_request.availableTimes = ''
        self._assert_lesson_request_is_invalid()

    def test_availableTimes_cannot_be_random_words(self):
        self.lesson_request.availableTimes = 'vjiweog'
        self._assert_lesson_request_is_invalid()

    def test_numberOfLessons_cannot_be_0(self):
        self.lesson_request.numberOfLessons = 0
        self._assert_lesson_request_is_invalid()

    def test_numberOfLessons_cannot_be_less_than_0(self):
        self.lesson_request.numberOfLessons = -20
        self._assert_lesson_request_is_invalid()

    def test_IntervalBetweenLessons_cannot_be_0(self):
        self.lesson_request.IntervalBetweenLessons = 0
        self._assert_lesson_request_is_invalid()

    def test_DurationOfLesson_cannot_be_0(self):
        self.lesson_request.DurationOfLesson = 0
        self._assert_lesson_request_is_invalid()

    def test_LearningObjectives_cannot_be_empty(self):
        self.lesson_request.LearningObjectives = ''
        self._assert_lesson_request_is_invalid()

    def test_AdditionalNotes_can_be_empty(self):
        self.lesson_request.AdditionalNotes = ''
        self._assert_lesson_request_is_valid()

    def test_FulFilled_cannot_be_empty(self):
        self.lesson_request.Fulfilled = ''
        self._assert_lesson_request_is_invalid()

    def _assert_lesson_request_is_valid(self):
        try:
            self.lesson_request.full_clean()
        except (ValidationError):
            self.fail('Test lesson request should be valid')

    def _assert_lesson_request_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.lesson_request.full_clean()



    
        
