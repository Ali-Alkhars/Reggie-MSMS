from django.test import TestCase
from lessons.forms import EditLoginsForm
from lessons.models import User

class EditLoginsFormTestCase(TestCase):
    """Unit tests of the EditLogins form"""

    fixtures = ['lessons/tests/fixtures/default_user.json']

    def setUp(self):
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': 'janedoe@example.org',
        }

    def test_form_has_necessary_fields(self):
        form = EditLoginsForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)

    def test_valid_user_form(self):
        form = EditLoginsForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_uses_email_validation(self):
        self.form_input['username'] = 'email@'
        form = EditLoginsForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        user = User.objects.get(username='johndoe@example.org')
        form = EditLoginsForm(instance=user, data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(user.username, 'janedoe@example.org')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
