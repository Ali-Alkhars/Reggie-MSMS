from django.core.management.base import BaseCommand
from faker import Faker
from lessons.models import Lesson_request, User
from django.contrib.auth.models import Group
from django.db.utils import IntegrityError 
import random
from lessons.helpers.helper_functions import create_invoice, record_payment


class Command(BaseCommand):
    PASSWORD = "Password123"
    UNFULFILLED = 15
    FULFILLED_PAID = 35
    FULFILLED_PARTIALLY_PAID = 12
    FULFILLED_UNPAID = 23
    FULFILLED_OVERPAID = 15

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')
        self.student = None

    def handle(self, *args, **options):
        student_count = 0
        self._create_specific_users()
        self._create_random_admin()
        print('3 Specific users and an extra admin are created')

        for i in range(Command.FULFILLED_PAID):
            print(f'Seeding student {student_count}',  end='\r')
            try:
                self._create_random_student_with_fulfilled_paid_request()
            except (IntegrityError):
                continue
            student_count += 1

        for i in range(Command.FULFILLED_PARTIALLY_PAID):
            print(f'Seeding student {student_count}',  end='\r')
            try:
                self._create_random_student_with_fulfilled_partially_paid_request()
            except (IntegrityError):
                continue
            student_count += 1

        for i in range(Command.FULFILLED_OVERPAID):
            print(f'Seeding student {student_count}',  end='\r')
            try:
                self._create_random_student_with_fulfilled_overpaid_request()
            except (IntegrityError):
                continue
            student_count += 1

        for i in range(Command.FULFILLED_UNPAID):
            print(f'Seeding student {student_count}',  end='\r')
            try:
                self._create_random_student_with_fulfilled_unpaid_request()
            except (IntegrityError):
                continue
            student_count += 1

        for i in range(Command.UNFULFILLED):
            print(f'Seeding student {student_count}',  end='\r')
            try:
                self._create_random_student_with_unfulfilled_request()
            except (IntegrityError):
                continue
            student_count += 1

        print('User seeding complete')

    def _create_random_student_with_unfulfilled_request(self):
        user = self._create_random_student()
        self._create_random_lesson(user)

    def _create_random_student_with_fulfilled_paid_request(self):
        user = self._create_random_student()
        lesson = self._create_random_lesson(user)
        lesson.Fulfilled = "Approved"
        lesson.save()
        invoice = create_invoice(lesson, user)
        record_payment(invoice.unpaid, invoice)

    def _create_random_student_with_fulfilled_partially_paid_request(self):
        user = self._create_random_student()
        lesson = self._create_random_lesson(user)
        lesson.Fulfilled = "Approved"
        lesson.save()
        invoice = create_invoice(lesson, user)
        record_payment(invoice.unpaid/2, invoice)

    def _create_random_student_with_fulfilled_unpaid_request(self):
        user = self._create_random_student()
        lesson = self._create_random_lesson(user)
        lesson.Fulfilled = "Approved"
        lesson.save()
        create_invoice(lesson, user)

    def _create_random_student_with_fulfilled_overpaid_request(self):
        user = self._create_random_student()
        lesson = self._create_random_lesson(user)
        lesson.Fulfilled = "Approved"
        lesson.save()
        invoice = create_invoice(lesson, user)
        record_payment(invoice.unpaid*2, invoice)

    def _create_random_student(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        username = self._username(first_name, last_name)
        user = User.objects.create_user(
            username,
            first_name=first_name,
            last_name=last_name,
            password=Command.PASSWORD,
        )
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(user)
        return user

    def _create_random_admin(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        username = self._username(first_name, last_name)
        user = User.objects.create_user(
            username,
            first_name=first_name,
            last_name=last_name,
            password=Command.PASSWORD,
        )
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(user)
        return user

    def _create_random_lesson(self, student):
        lesson = Lesson_request.objects.create(
            student=student,
            availableDays='Tuesday',
            numberOfLessons=random.randint(1,10),
            IntervalBetweenLessons=random.randint(1,3),
            DurationOfLesson= 60,
            LearningObjectives= 'Learn to play the piano',
            AdditionalNotes= f'I want Mr. {self.faker.last_name()} to teach me'
        )
        return lesson

    def _create_specific_director(self):
        first_name = 'Marty'
        last_name = 'Major'
        username = 'marty.major@example.org'
        user = User.objects.create_user(
            username,
            first_name=first_name,
            last_name=last_name,
            password=Command.PASSWORD,
        )
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(user)

    def _create_specific_admin(self):
        first_name = 'Petra'
        last_name = 'Pickles'
        username = 'petra.pickles@example.org'
        user = User.objects.create_user(
            username,
            first_name=first_name,
            last_name=last_name,
            password=Command.PASSWORD,
        )
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(user)

    def _create_specific_student(self):
        first_name = 'John'
        last_name = 'Doe'
        username = 'john.doe@example.org'
        user = User.objects.create_user(
            username,
            first_name=first_name,
            last_name=last_name,
            password=Command.PASSWORD,
        )
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(user)
        first_lesson = self._create_random_lesson(user)
        first_lesson.Fulfilled = "Approved"
        first_lesson.save()
        invoice = create_invoice(first_lesson, user)
        record_payment(invoice.unpaid, invoice)
        self._create_random_lesson(user)

    def _create_specific_users(self):
        self._create_specific_director()
        self._create_specific_admin()


    def _username(self, first_name, last_name):
        username = f'{first_name}{last_name}@example.org'
        return username