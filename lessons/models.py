from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MaxValueValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

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

fulfilled_choices = [
    ('Approved', 'Approved'),
    ('Denied', 'Denied'),
    ('Pending', 'Pending'),
]

value_choices = [
]
for i in range(1, 17):
    value_choices.append((15*i,'{} minutes'.format(15*i)))

# Make sure values are not non-zero
def validate_nonzero(value):
    if (value <= 0):
        raise ValidationError(
            ('%(value) is not allowed'),
            params={'value':value},
        )


class Lesson_request(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    availableDays = models.CharField(max_length=100, blank=False, choices=weekday_choices)
    availableTimes = models.CharField(max_length=255, blank=False, choices=time_choices)
    # availableDays = models.ManyToManyField(Weekdays_Choices, symmetrical=False)
    # availableTimes = models.ManyToManyField(Time_Choices, symmetrical=False)
    numberOfLessons = models.PositiveIntegerField(blank=False, validators=[validate_nonzero])
    IntervalBetweenLessons = models.PositiveIntegerField(blank=False, validators=[validate_nonzero])
    DurationOfLesson = models.PositiveIntegerField(blank = False, validators=[validate_nonzero], choices=value_choices)
    LearningObjectives = models.TextField(blank=False)
    AdditionalNotes = models.TextField(blank=True)
    Fulfilled = models.CharField(max_length=50, blank=False, choices=fulfilled_choices, default='Pending')

    def getWeekdays_choices():
        return weekday_choices
    
    def getTime_choices():
        return time_choices
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
    student = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
