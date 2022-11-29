from django.test import TestCase
from django.urls import reverse
from lessons.models import User
from lessons.management.commands.create_user_groups import Command



class HomePageRedirectsTest(TestCase):

    fixtures = ['lessons/tests/fixtures/default_user.json']

    def setUp(self):

        create_groups_command = Command()
        create_groups_command.handle()
        self.user = User.objects.get(username= "johndoe@example.org")
        self.client.login(username = self.user.username, password = "Password123")
        self.url=reverse('home')


    def test_home_url(self):
        self.assertEqual(self.url, '/home/')

    def test_get_bookings(self):
        response = self.client.post(reverse('bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings.html')

    def test_get_home(self):
        response = self.client.post(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
