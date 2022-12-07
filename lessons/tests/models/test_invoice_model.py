from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from lessons.models import Invoice, Lesson_request, User
from django.contrib.auth.models import Group
from lessons.management.commands.create_user_groups import Command
from django.utils import timezone
from datetime import timedelta

class InvoiceModelTestCase(TestCase):
    """Unit tests for the Invoice model."""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json',
        'lessons/tests/fixtures/default_lesson_request.json'
    ]
    
    def setUp(self):
        create_groups_command = Command()
        create_groups_command.handle()
        self.lesson = Lesson_request.objects.get(AdditionalNotes= "I know how to play piano.")
        self.student = User.objects.get(username= "johndoe@example.org")
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(self.student)
        self.invoice = Invoice.objects.create (
            reference= f"{self.student.id}-001",
            price= 19,
            unpaid= 19,
            creation_date= timezone.now(),
            update_date= timezone.now(),
            student= self.student,
            lesson= self.lesson
        )

    def test_valid_invoice(self):
        self._assert_invoice_is_valid()

    def test_reference_cannot_be_blank(self):
        self.invoice.reference = ''
        self._assert_invoice_is_invalid()

    def test_reference_cannot_have_letters(self):
        self.invoice.reference = 'fail-00'
        self._assert_invoice_is_invalid()
        self.invoice.reference = '00-fail'
        self._assert_invoice_is_invalid()

    def test_reference_cannot_have_symbols_other_than_dash(self):
        self.invoice.reference = '01/00'
        self._assert_invoice_is_invalid()
        self.invoice.reference = '01!00'
        self._assert_invoice_is_invalid()
        self.invoice.reference = '01@00'
        self._assert_invoice_is_invalid()
        self.invoice.reference = '01#00'
        self._assert_invoice_is_invalid()
        self.invoice.reference = '01$00'
        self._assert_invoice_is_invalid()
        self.invoice.reference = '01_00'
        self._assert_invoice_is_invalid()

    def test_reference_cannot_be_longer_than_50_characters(self):
        self.invoice.reference = ('2' *25) + '-' + ('3'*25)
        self._assert_invoice_is_invalid()

    def test_reference_can_be_50_characters(self):
        self.invoice.reference = ('2' *25) + '-' + ('3'*24)
        self._assert_invoice_is_valid()

    def test_reference_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            invoice = Invoice.objects.create (
                reference= f"{self.student.id}-001",
                price= 19,
                unpaid= 10,
                creation_date= timezone.now(),
                update_date= timezone.now(),
                student= self.student,
                lesson= self.lesson
            )
            invoice.full_clean()

    def test_price_cannot_be_blank(self):
        with self.assertRaises(IntegrityError):
            invoice = Invoice.objects.create (
                reference= f"{self.student.id}-002",
                unpaid= 10,
                creation_date= timezone.now(),
                update_date= timezone.now(),
                student= self.student
            )
            invoice.full_clean()
    
    def test_price_cannot_be_string(self):
        self.invoice.price = 'fail'
        self._assert_invoice_is_invalid()

    def test_price_cannot_be_more_than_100k(self):
        self.invoice.price = 1000001
        self._assert_invoice_is_invalid()

    def test_price_can_be_100k(self):
        self.invoice.price = 1000000
        self._assert_invoice_is_valid()

    def test_price_can_be_integer(self):
        self.invoice.price = 5
        self._assert_invoice_is_valid()

    def test_price_can_be_decimal(self):
        self.invoice.price = 5.5
        self._assert_invoice_is_valid()

    def test_unpaid_cannot_be_blank(self):
        with self.assertRaises(IntegrityError):
            invoice = Invoice.objects.create (
                reference= f"{self.student.id}-002",
                price= 19,
                creation_date= timezone.now(),
                update_date= timezone.now(),
                student= self.student,
                lesson= self.lesson
            )
            invoice.full_clean()
    
    def test_unpaid_cannot_be_string(self):
        self.invoice.unpaid = 'fail'
        self._assert_invoice_is_invalid()

    def test_unpaid_cannot_be_more_than_100k(self):
        self.invoice.unpaid = 1000001
        self._assert_invoice_is_invalid()

    def test_unpaid_can_be_100k(self):
        self.invoice.unpaid = 1000000
        self._assert_invoice_is_valid()

    def test_unpaid_can_be_integer(self):
        self.invoice.unpaid = 5
        self._assert_invoice_is_valid()

    def test_unpaid_can_be_decimal(self):
        self.invoice.unpaid = 5.5
        self._assert_invoice_is_valid()

    def test_creation_date_cannot_be_a_string(self):
        self.invoice.creation_date = '02/12/2022'
        self._assert_invoice_is_invalid()

    def test_creation_date_cannot_be_blank(self):
        with self.assertRaises(IntegrityError):
            invoice = Invoice.objects.create (
                reference= f"{self.student.id}-002",
                price= 19,
                unpaid=10,
                update_date= timezone.now(),
                student= self.student,
                lesson= self.lesson
            )
            invoice.full_clean()

    def test_creation_date_cannot_be_in_the_future(self):
        self.invoice.creation_date = timezone.now() + timedelta(days=1)
        self._assert_invoice_is_invalid()

    def test_update_date_cannot_be_a_string(self):
        self.invoice.update_date = '02/12/2022'
        self._assert_invoice_is_invalid()

    def test_update_date_cannot_be_blank(self):
        with self.assertRaises(IntegrityError):
            invoice = Invoice.objects.create (
                reference= f"{self.student.id}-002",
                price= 19,
                unpaid=10,
                creation_date= timezone.now(),
                student= self.student,
                lesson= self.lesson
            )
            invoice.full_clean()

    def test_update_date_cannot_be_in_the_future(self):
        self.invoice.update_date = timezone.now() + timedelta(days=1)
        self._assert_invoice_is_invalid()

    def test_student_cannot_be_blank(self):
        self.invoice.student = None
        self._assert_invoice_is_invalid()

    def test_lesson_cannot_be_blank(self):
        self.invoice.lesson = None
        self._assert_invoice_is_invalid()

    def test_deleting_student_deletes_invoice(self):
        user_count_before = len(User.objects.all())
        invoice_count_before = len(Invoice.objects.all())
        self.student.delete()
        user_count_after = len(User.objects.all())
        invoice_count_after = len(Invoice.objects.all())
        self.assertEqual(user_count_before, user_count_after+1)
        self.assertEqual(invoice_count_before, invoice_count_after+1)

    def _assert_invoice_is_valid(self):
        try:
            self.invoice.full_clean()
        except (ValidationError):
            self.fail('Test invoice should be valid')

    def _assert_invoice_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.invoice.full_clean()