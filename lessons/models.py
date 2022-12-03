from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings


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


class LessonRequest(models.Model):

    class Availability(models.IntegerChoices):
        Once = 1, 'Once a week'
        Twice = 2, 'Twice a week'

    class Duration(models.IntegerChoices):
        HalfHour = 30, '30 min'
        ThreeQuarters = 45, '45 min'
        Hour = 60, '60 min'

    availability = models.IntegerField(
        choices=Availability.choices,
        default=Availability.Once
    )
    duration = models.IntegerField(
        choices=Duration.choices,
        default=Duration.HalfHour
    )
    preferredTeacher = models.CharField(max_length=20)
    additionalInfo = models.TextField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE
    )

    booked = models.BooleanField(
        default=False
    )
