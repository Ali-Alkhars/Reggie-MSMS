from django.test import TestCase
from lessons.models import User
from lessons.forms import EditPasswordForm

class EditPasswordFormTestCase(TestCase):

    fixtures = ['lessons/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.form_input = {
            'current_password': 'Password123',
            'new_password': 'NewPassword123',
            'confirm_password': 'NewPassword123',
        }

    def test_form_has_necessary_fields(self):
        form = EditPasswordForm()
        self.assertIn('current_password', form.fields)
        self.assertIn('new_password', form.fields)
        self.assertIn('confirm_password', form.fields)

    def test_valid_form(self):
        form = EditPasswordForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_password_must_contain_uppercase_character(self):
        self.form_input['new_password'] = 'password123'
        self.form_input['confirm_password'] = 'password123'
        form = EditPasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.form_input['new_password'] = 'PASSWORD123'
        self.form_input['confirm_password'] = 'PASSWORD123'
        form = EditPasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['new_password'] = 'PasswordABC'
        self.form_input['confirm_password'] = 'PasswordABC'
        form = EditPasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_and_confirm_password_are_identical(self):
        self.form_input['confirm_password'] = 'WrongPassword123'
        form = EditPasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())
