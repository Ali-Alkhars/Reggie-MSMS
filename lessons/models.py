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

    def isStudent(self):
        """True if the user is a student"""
        return self.groups.all()[0].name == 'student'

    def isAdmin(self):
        """True if the user is an admin"""
        return self.groups.all()[0].name == 'admin'

    def isDirector(self):
        """True if the user is a director"""
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
    price = models.FloatField(max_length=20, blank=False)
    unpaid = models.FloatField(max_length=20, blank=False)
    creation_date = models.DateTimeField(blank=False)
    update_date = models.DateTimeField(blank=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
