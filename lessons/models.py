from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MaxValueValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime

class User(AbstractUser):
    """User model used for creating different users in the MSMS."""

    username = models.CharField(
        max_length=80,
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

    def isStudent(self):
        """True if groups are created and the user is a student"""
        if not self.groups.exists():
            return False
        return self.groups.all()[0].name == 'student'

    def isAdmin(self):
        """True if groups are created and the user is an admin"""
        if not self.groups.exists():
            return False
        return self.groups.all()[0].name == 'admin'

    def isDirector(self):
        """True if groups are created and the user is a director"""
        if not self.groups.exists():
            return False
        return self.groups.all()[0].name == 'director'


WEEKDAY_CHOICES = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
]

TIME_CHOICES = [
    ('Morning', 'Morning'),
    ('Afternoon', 'Afternoon'),
    ('Night', 'Night'),
]

VALUE_CHOICES = [
    (15, '15 minutes'),
    (30, '30 minutes'),
    (45, '45 minutes'),
    (60, '60 minutes'),
    (75, '75 minutes'),
    (90, '90 minutes'),
    (105, '105 minutes'),
    (120, '120 minutes'),
]

TERM_ORDER = [
    ('First term', 'First term'),
    ('Second term', 'Second term'),
]

# Make sure values are not non-zero
def validate_nonzero(value):
    if (value <= 0):
        raise ValidationError(
            ('%(value) is not allowed'),
            params={'value':value},
        )


class Lesson_request(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    availableDays = models.CharField(max_length=100, blank=False, choices=WEEKDAY_CHOICES)
    availableTimes = models.CharField(max_length=255, blank=False, choices=TIME_CHOICES)
    numberOfLessons = models.PositiveIntegerField(blank=False, validators=[validate_nonzero])
    IntervalBetweenLessons = models.PositiveIntegerField(blank=False, validators=[validate_nonzero])
    DurationOfLesson = models.PositiveIntegerField(blank = False, validators=[validate_nonzero], choices=VALUE_CHOICES)
    LearningObjectives = models.TextField(blank=False)
    AdditionalNotes = models.TextField(blank=True)
    Fulfilled = models.CharField(max_length=50, blank=False, default='Pending')

    def getWeekdays_choices():
        return WEEKDAY_CHOICES
    
    def getTime_choices():
        return TIME_CHOICES

class Invoice(models.Model):
    """Invoice model used to create invoices of bank transfers for the lesson payments"""

    reference = models.CharField(
        unique=True, 
        blank=False, 
        max_length=50, 
        primary_key=True, 
        validators= [RegexValidator(
            regex='^[0-9-]*$',
            message= 'Reference number should be numbers-numbers',
            code='invalid_reference'
        )]
    )
    price = models.FloatField(blank=False, validators= [MaxValueValidator(1000000)])
    unpaid = models.FloatField(blank=False, validators= [MaxValueValidator(1000000)])
    creation_date = models.DateTimeField(blank=False, validators=[MaxValueValidator(limit_value=timezone.now)])
    update_date = models.DateTimeField(blank=False, validators=[MaxValueValidator(limit_value=timezone.now)])
    student = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    lesson = models.ForeignKey(Lesson_request, on_delete=models.CASCADE, blank=False, null=True)

class TermTime(models.Model):
    startDate = models.DateField(help_text="Enter a date after now", blank=False, unique = True)
    endDate = models.DateField(help_text="Enter a date after now and after start date", blank=False, unique=True)
    midTerm = models.DateField(blank=False, default="2020-01-01")
    termOrder = models.CharField(max_length=100, blank=False, choices=TERM_ORDER, default="First Term")

