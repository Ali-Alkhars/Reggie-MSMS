from django.conf import settings
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from lessons.models import Invoice, User
from lessons.management.commands.create_user_groups import Command
from lessons.tests.helpers import reverse_with_next
from django.utils import timezone

class StudentInvoicesViewTestCase(TestCase):
    """Tests of the student_invoices view."""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        create_groups_command = Command()
        create_groups_command.handle()
        self.user = User.objects.get(username= "johndoe@example.org")
        self.student = User.objects.get(username= "janedoe@example.org")
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(self.student)
        self.invoice = Invoice.objects.create (
            reference= f"{self.student.id}-001",
            price= 19,
            unpaid= 19,
            creation_date= timezone.now(),
            update_date= timezone.now(),
            student= self.student
        )
        self.url = reverse('student_invoices', kwargs={'user_id': self.student.id})

    def test_student_invoices_url(self):
        self.assertEqual(self.url, f'/student_invoices/{self.student.id}')

    def test_get_student_invoices_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_student_invoices(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_invoices.html')
        invoices = response.context['invoices']
        self.assertEqual(len(invoices), 1)
        self.assertEqual(invoices[0].reference, self.invoice.reference)

    def test_get_student_invoices_with_more_than_one_invoice(self):
        self.client.login(username=self.user.username, password='Password123')
        self._create_invoices(9)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_invoices.html')
        invoices = response.context['invoices']
        self.assertEqual(len(invoices), 10)

    def _create_invoices(self, count=10):
        for i in range(count):
            Invoice.objects.create (
            reference= f"{self.student.id}-{i}",
            price= 19,
            unpaid= 10,
            creation_date= timezone.now(),
            update_date= timezone.now(),
            student= self.student
        )

