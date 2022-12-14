"""Unit tests for the User model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from lessons.models import User

class UserModelTestCase(TestCase):
    """Unit tests for the User model."""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json'
    ]
    
    def setUp(self):
        self.user = User.objects.get(username= "johndoe@example.org")

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_username_cannot_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()

    def test_username_can_contain_two_dots_after_at(self):
        self.user.username = 'johndoe@example.co.uk'
        self._assert_user_is_valid()

    def test_username_may_contain_80_characters(self):
        self.user.username = ('x' * 30) + '@' + ('y' * 45) + '.com'
        self._assert_user_is_valid()

    def test_username_must_not_contain_more_than_80_characters(self):
        self.user.username = ('x' * 30) + '@' + ('y' * 46) + '.com'
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        second_user = User.objects.get(username = "janedoe@example.org")
        self.user.username = second_user.username
        self._assert_user_is_invalid()

    def test_username_must_contain_name(self):
        self.user.username = '@example.org'
        self._assert_user_is_invalid()

    def test_username_must_contain_at_symbol(self):
        self.user.username = 'johndoe.example.org'
        self._assert_user_is_invalid()

    def test_username_must_contain_domain_name(self):
        self.user.username = 'johndoe@.org'
        self._assert_user_is_invalid()

    def test_username_must_contain_domain(self):
        self.user.username = 'johndoe@example'
        self._assert_user_is_invalid()

    def test_username_must_not_contain_more_than_one_at(self):
        self.user.username = 'johndoe@@example.org'
        self._assert_user_is_invalid()

    def test_first_name_must_not_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_need_not_be_unique(self):
        second_user = User.objects.get(username = "janedoe@example.org")
        self.user.first_name = second_user.first_name
        self._assert_user_is_valid()

    def test_first_name_may_contain_20_characters(self):
        self.user.first_name = 'x' * 20
        self._assert_user_is_valid()

    def test_first_name_must_not_contain_more_than_20_characters(self):
        self.user.first_name = 'x' * 21
        self._assert_user_is_invalid()

    def test_last_name_must_not_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()

    def test_last_name_need_not_be_unique(self):
        second_user = User.objects.get(username = "janedoe@example.org")
        self.user.last_name = second_user.last_name
        self._assert_user_is_valid()

    def test_last_name_may_contain_20_characters(self):
        self.user.last_name = 'x' * 20
        self._assert_user_is_valid()

    def test_last_name_must_not_contain_more_than_20_characters(self):
        self.user.last_name = 'x' * 21
        self._assert_user_is_invalid()


    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()
