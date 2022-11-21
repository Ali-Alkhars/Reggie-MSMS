from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError


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

# Make sure values are not non-zero
def validate_nonzero(value):
    if value ==0:
        raise ValidationError(
            ('%(value) is not allowed'),
            params={'value':value},
        )
class Lesson_request(models.Model):
    availableDays = models.CharField(max_length=100, blank=False, choices=weekday_choices)
    availableTimes = models.CharField(max_length=255, blank=False, choices=time_choices)
    numberOfLessons = models.PositiveIntegerField(blank=False, validators=[validate_nonzero]);
    IntervalBetweenLessons = models.PositiveIntegerField(blank=False, validators=[validate_nonzero]);
    DurationOfLesson = models.PositiveIntegerField(blank = False, validators=[validate_nonzero]);
    LearningObjectives = models.CharField(max_length= 255, blank=True);
    AdditionalNotes = models.CharField(max_length = 255, blank=True);

