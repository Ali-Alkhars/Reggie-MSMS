from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """User model used for creating different users in the MSMS."""

    username = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex='[a-z0-9]+@[a-z]+\.[a-z]{2,3}',
                message='Username must be an Email',
                code='invalid_username'
            )
        ]
    )
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)

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
class Lesson_request(models.Model):
    availableDays = models.CharField(max_length=100, blank=False, choices=weekday_choices)
    availableTimes = models.CharField(max_length=255, blank=False, choices=time_choices)
    numberOfLessons = models.PositiveIntegerField(blank=False);
    IntervalBetweenLessons = models.PositiveIntegerField(blank=False);
    DurationOfLesson = models.PositiveIntegerField(blank = False);
    LearningObjectives = models.CharField(max_length= 255);
    AdditionalNotes = models.CharField(max_length = 255);

