from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from lessons.models import User
from django.contrib.auth.models import Group


class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self._create_user()


    def _create_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        username = 'chinwan@gmail.com'
        user = User.objects.create_user(
            username,
            first_name=first_name,
            last_name=last_name,
            password='Password123',
        )
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(user)

    def _email(self, first_name, last_name):
        email = f'{first_name}.{last_name}@example.org'
        return email
