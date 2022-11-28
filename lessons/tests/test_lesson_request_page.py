"""Unit tests for the lesson request page."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from lessons.models import Lesson_request
from lessons.forms import LessonRequestForm

class LessonRequestPageTestCase(TestCase):
    """Unit tests for the lesson request page"""

    fixtures = [
        'lessons/tests/fixtures/default_lesson_request.json'
    ]

    def setUp(self):
        self.url = reverse('lesson_request')
        # Can change to student foreign key when implemented
        self.lesson_request = Lesson_request.objects.get(AdditionalNotes= "I know how to play piano.")

    def test_lesson_request_url(self):
        self.assertEqual(self.url, '/lesson_request/')

    def test_lesson_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lesson_request.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LessonRequestForm))
        self.assertFalse(form.is_bound)

    def test_post_lesson_request_with_blank_days(self):
        form_input = {
            'availableDays': "", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        before_count = Lesson_request.objects.count()
        response = self.client.post(self.url, form_input, follow=True)
        after_count = Lesson_request.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lesson_request.html')
    
    def successful_lesson_request(self):
        form_input = {
            'availableDays': "Monday", 
            'availableTimes': 'Night',
            "numberOfLessons": 1,
            "IntervalBetweenLessons": 5,
            "DurationOfLesson": 30,
            "LearningObjectives": "I want to learn music.",
            "AdditionalNotes": "I know how to play violin"
        }
        before_count = Lesson_request.objects.count()
        response = self.client.post(self.url, form_input, follow=True)
        after_count = Lesson_request.objects.count()
        self.assertEqual(after_count, before_count+1)
        redirect_url = reverse('lesson_page')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'lesson_page.html')
        # Can change to student foreign key when implemented
        lesson = Lesson_request.objects.get(AdditionalNotes="I know how to play violin")
        self.assertEqual(lesson.availableDays, 'Monday')
        self.assertEqual(lesson.availableTimes, 'Night')
        self.assertEqual(lesson.numberOfLessons, 1)
        self.assertEqual(lesson.IntervalBetweenLessons, 5)
        self.assertEqual(lesson.DurationOfLesson, 30)
        self.assertEqual(lesson.LearningObjectives, "I want to learn music.")
        self.assertEqual(lesson.AdditionalNotes, "I know how to play violin")




       

        