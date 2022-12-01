from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


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

class Invoice(models.Model):
    """Invoice model used to create invoices of bank transfers for the lesson payments"""

    reference = models.CharField(unique=True, blank=False, max_length=50)
    price = models.CharField(max_length=20)
    unpaid = models.CharField(max_length=20)
    creation_date = models.DateTimeField()
    update_date = models.DateTimeField()
    student = models.ForeignKey(User, on_delete=models.CASCADE)

