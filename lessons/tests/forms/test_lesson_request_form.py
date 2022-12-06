from django.test import TestCase
from lessons.forms import EditLoginsForm, LessonRequestForm
from lessons.models import User

class LessonRequestFormTestCase(TestCase):
    """Unit tests of the lesson request form"""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json',
        'lessons/tests/fixtures/default_lesson_request.json'
    ]

    def setUp(self):
        self.form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin",
            "Fulfilled": "Pending"
        }
    
    def test_form_contains_required_fields(self):
        form = LessonRequestForm()
        self.assertIn('availableDays', form.fields)
        self.assertIn('availableTimes', form.fields)
        self.assertIn('numberOfLessons', form.fields)
        self.assertIn('IntervalBetweenLessons', form.fields)
        self.assertIn('DurationOfLesson', form.fields)
        self.assertIn('LearningObjectives', form.fields)
        self.assertIn('AdditionalNotes', form.fields)
    
    def test_form_accept_valid_input(self):
        form = LessonRequestForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_reject_blank_available_days(self):
        self.form_input['availableDays'] = ''
        form = LessonRequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_reject_blank_available_times(self):
        self.form_input['availableTimes'] = ''
        form = LessonRequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_reject_zero_number_of_lessons(self):
        self.form_input['numberOfLessons'] = 0
        form = LessonRequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_reject_negative_number_of_lessons(self):
        self.form_input['numberOfLessons'] = -20
        form = LessonRequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_reject_zero_interval_between_lessons(self):
        self.form_input['IntervalBetweenLessons'] = 0
        form = LessonRequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_reject_negative_interval_between_lessons(self):
        self.form_input['IntervalBetweenLessons'] = -20
        form = LessonRequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_reject_zero_duration_of_lesson(self):
        self.form_input['DurationOfLesson'] = 0
        form = LessonRequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_reject_negative_duration_of_lesson(self):
        self.form_input['DurationOfLesson'] = -20
        form = LessonRequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_reject_blank_learning_objectives(self):
        self.form_input['LearningObjectives'] = ''
        form = LessonRequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_accept_blank_additional_notes(self):
        self.form_input['additionalNotes'] = ''
        form = LessonRequestForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    
    
    
    
    
    



