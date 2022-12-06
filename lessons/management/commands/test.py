from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from django.contrib.auth.models import Group
from lessons.models import User


class Command(BaseCommand):
    PASSWORD = "Password123"
    USER_COUNT = 100

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        user_count = 0
        while user_count < Command.USER_COUNT:
            print(f'Seeding user {user_count}',  end='\r')
            try:
                self._create_user()
            except (django.db.utils.IntegrityError):
                continue
            user_count += 1
        print('User seeding complete')

    def _create_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        username = self._username(first_name, last_name)
        return User.objects.create_user(
            username,
            first_name=first_name,
            last_name=last_name,
            password=Command.PASSWORD,
        )
    
    def _create_student(self):
        user = self._create_user()
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(user)

    def _create_admin(self):
        user = self._create_admin()
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(user)

    def _create_director(self):
        user = self._create_director()
        director_group = Group.objects.get(name='director')
        director_group.user_set.add(user)

    def _username(self, first_name, last_name):
        username = f'{first_name}{last_name}@example.org'
        return username