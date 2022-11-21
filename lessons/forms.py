from django import forms
from .models import Lesson_request

weekday_choices = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
]

time_choices = [
    ('Morning', 'Morning'),
    ('Afternoon', 'Afternoon'),
    ('Night', 'Night'),
]


# Request form for the lesson
class LessonRequestForm(forms.ModelForm):
    class Meta:
        model = Lesson_request
        fields = ["availableDays", "availableTimes", "numberOfLessons", "IntervalBetweenLessons", "DurationOfLesson", "LearningObjectives", "AdditionalNotes"]
        labels = {
            'availableDays': "Available days: ",
            'availableTimes': "Available times: ",
            'numberOfLessons': "Number of lessons desired: ",
            'IntervalBetweenLessons': "Interval between lessons (In weeks): ",
            'DurationOfLesson': "Duration of lesson (In minutes): ",
            'LearningObjectives': "What do you want to learn? ",
            'AdditionalNotes': "Additional notes/comments: " 
        }
        widget = {
            "LearningObjectives": forms.Textarea(),
            "AdditionalNotes": forms.Textarea()
        }







