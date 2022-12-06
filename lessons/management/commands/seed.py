from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from lessons.models import Invoice, User
from django.contrib.auth.models import Group
from django.utils import timezone
from django.db.utils import IntegrityError 


class Command(BaseCommand):
    PASSWORD = "Password123"
    USER_COUNT = 100

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')
        self.student = None

    def handle(self, *args, **options):
        user_count = 0
        while user_count < Command.USER_COUNT:
            print(f'Seeding user {user_count}',  end='\r')
            try:
                self._create_student()
            except (IntegrityError):
                continue
            user_count += 1
        print('User seeding complete')
        self.student = self._create_student()
        self._create_director()
        self._create_invoices()

    def _create_invoices(self):
        Invoice.objects.create (
            reference= f"{self.student.id}-001",
            price= 19,
            unpaid= 19,
            creation_date= timezone.now(),
            update_date= timezone.now(),
            student= self.student
        )
        Invoice.objects.create (
            reference= f"{self.student.id}-002",
            price= 19,
            unpaid= 0,
            creation_date= timezone.now(),
            update_date= timezone.now(),
            student= self.student
        )
        Invoice.objects.create (
            reference= f"{self.student.id}-003",
            price= 19,
            unpaid= 10,
            creation_date= timezone.now(),
            update_date= timezone.now(),
            student= self.student
        )
        Invoice.objects.create (
            reference= f"{self.student.id}-004",
            price= 19,
            unpaid= -6,
            creation_date= timezone.now(),
            update_date= timezone.now(),
            student= self.student
        )
        

    def _create_student(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        username = self._username(first_name, last_name)
        user = User.objects.create_user(
            username,
            first_name=first_name,
            last_name=last_name,
            password='Password123',
        )
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(user)
        return user

    def _create_director(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        username = 'director@invoice.com'
        user = User.objects.create_user(
            username,
            first_name=first_name,
            last_name=last_name,
            password='Password123',
        )
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(user)

    def _email(self, first_name, last_name):
        email = f'{first_name}.{last_name}@example.org'
        return email

    def _username(self, first_name, last_name):
        username = f'{first_name}{last_name}@example.org'
        return username