from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from lessons.forms import RegisterForm
from lessons.models import User
from lessons.management.commands.create_user_groups import Command

class RegisterFormTestCase(TestCase):
    """Unit tests of the sign up form."""

    def setUp(self):
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': 'janedoe@example.org',
            'new_password': 'Password123',
            'confirm_password': 'Password123'
        }

    def test_valid_register_form(self):
        form = RegisterForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = RegisterForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        self.assertIn('new_password', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
        self.assertIn('confirm_password', form.fields)
        confirm_password_widget = form.fields['confirm_password'].widget
        self.assertTrue(isinstance(confirm_password_widget, forms.PasswordInput))

    def test_form_uses_model_validation(self):
        self.form_input['username'] = 'badusername'
        form = RegisterForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_uppercase_character(self):
        self.form_input['new_password'] = 'password123'
        self.form_input['confirm_password'] = 'password123'
        form = RegisterForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.form_input['new_password'] = 'PASSWORD123'
        self.form_input['confirm_password'] = 'PASSWORD123'
        form = RegisterForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['new_password'] = 'PasswordABC'
        self.form_input['confirm_password'] = 'PasswordABC'
        form = RegisterForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_and_password_confirmation_are_identical(self):
        self.form_input['confirm_password'] = 'WrongPassword123'
        form = RegisterForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        create_groups_command = Command()
        create_groups_command.handle()

        form = RegisterForm(data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)

        user = User.objects.get(username='janedoe@example.org')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        is_password_correct = check_password('Password123', user.password)
        self.assertEqual(user.groups.all()[0].name, 'student')

        self.assertTrue(is_password_correct)
