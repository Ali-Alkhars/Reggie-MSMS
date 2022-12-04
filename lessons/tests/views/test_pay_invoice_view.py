from django.conf import settings
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from lessons.models import Invoice, User
from lessons.management.commands.create_user_groups import Command
from lessons.tests.helpers import reverse_with_next
from django.utils import timezone

class PayInvoiceViewTestCase(TestCase):
    """Tests of the pay_invoice view."""

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
            price= 20,
            unpaid= 20,
            creation_date= timezone.now(),
            update_date= timezone.now(),
            student= self.student
        )
        self.url = reverse('pay_invoice', kwargs={'reference': self.invoice.reference})

    def test_pay_invoice_url(self):
        self.assertEqual(self.url, f'/pay_invoice/{self.invoice.reference}')

    def test_half_pay_invoice_as_director(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        response = self.client.post(self.url, data={'paid': 10}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pay_invoice.html')
        invoice = response.context['invoice']
        self.assertEqual(invoice.reference, self.invoice.reference)
        self.assertEqual(invoice.unpaid, 10)
        self.assertNotEqual(invoice.update_date, invoice.creation_date)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_half_pay_invoice_as_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(self.user)
        response = self.client.post(self.url, data={'paid': 10}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pay_invoice.html')
        invoice = response.context['invoice']
        self.assertEqual(invoice.reference, self.invoice.reference)
        self.assertEqual(invoice.unpaid, 10)
        self.assertNotEqual(invoice.update_date, invoice.creation_date)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_fully_pay_invoice_as_director(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        response = self.client.post(self.url, data={'paid': 20}, follow=True)
        self.invoice = Invoice.objects.get(reference=self.invoice.reference)
        self.assertEqual(self.invoice.unpaid, 0)
        self.assertNotEqual(self.invoice.update_date, self.invoice.creation_date)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(response.status_code, 200)
        redirect_url = reverse('student_invoices', kwargs={'user_id': self.invoice.student.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student_invoices.html')

    def test_fully_pay_invoice_as_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(self.user)
        response = self.client.post(self.url, data={'paid': 20}, follow=True)
        self.invoice = Invoice.objects.get(reference=self.invoice.reference)
        self.assertEqual(self.invoice.unpaid, 0)
        self.assertNotEqual(self.invoice.update_date, self.invoice.creation_date)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(response.status_code, 200)
        redirect_url = reverse('student_invoices', kwargs={'user_id': self.invoice.student.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student_invoices.html')

    def test_overpay_invoice_as_director(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        response = self.client.post(self.url, data={'paid': 30}, follow=True)
        self.invoice = Invoice.objects.get(reference=self.invoice.reference)
        self.assertEqual(self.invoice.unpaid, -10)
        self.assertNotEqual(self.invoice.update_date, self.invoice.creation_date)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(response.status_code, 200)
        redirect_url = reverse('student_invoices', kwargs={'user_id': self.invoice.student.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student_invoices.html')

    def test_overpay_invoice_as_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(self.user)
        response = self.client.post(self.url, data={'paid': 30}, follow=True)
        self.invoice = Invoice.objects.get(reference=self.invoice.reference)
        self.assertEqual(self.invoice.unpaid, -10)
        self.assertNotEqual(self.invoice.update_date, self.invoice.creation_date)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(response.status_code, 200)
        redirect_url = reverse('student_invoices', kwargs={'user_id': self.invoice.student.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student_invoices.html')
    
    def test_get_pay_invoice_as_director(self):
        self.client.login(username=self.user.username, password='Password123')
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pay_invoice.html')
        invoice = response.context['invoice']
        self.assertEqual(invoice.reference, self.invoice.reference)

    def test_get_pay_invoice_as_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pay_invoice.html')
        invoice = response.context['invoice']
        self.assertEqual(invoice.reference, self.invoice.reference)

    def test_get_pay_invoice_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.url)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_pay_invoice_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next(settings.LOGIN_URL, self.url)
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_logged_in_student_cannot_access_pay_invoice_page(self):
        self.client.login(username = self.user.username, password = "Password123")
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)