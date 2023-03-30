from unittest import TestCase

from pydantic import ValidationError

from app.user.schema import User, UserBase


class TestUser(TestCase):

    def test_empty_constructor(self):
        with self.assertRaises(ValidationError):
            User()

    def test_invalid_account(self):
        with self.assertRaises(ValidationError) as cm:
            User(account="12345", password="123456", email="a@gmail.com", name="n")
        msg = str(cm.exception)
        self.assertIn("account", msg)
        self.assertIn("ensure this value has at least 6 characters", msg)

    def test_invalid_password(self):
        with self.assertRaises(ValidationError) as cm:
            User(account="123456", password="12345", email="a@gmail.com", name="n")
        msg = str(cm.exception)
        self.assertIn("password", msg)
        self.assertIn("ensure this value has at least 6 characters", msg)

    def test_invalid_name(self):
        with self.assertRaises(ValidationError) as cm:
            User(account="123456", password="123456", email="a@gmail.com", name="")
        msg = str(cm.exception)
        self.assertIn("name", msg)
        self.assertIn("ensure this value has at least 1 character", msg)

    def test_invalid_email(self):
        with self.assertRaises(ValidationError) as cm:
            User(account="123456", password="123456", email="@gmail.com", name="n")
        msg = str(cm.exception)
        self.assertIn("email", msg)
        self.assertIn("value is not a valid email address", msg)

    def test_create_user(self):
        user = UserBase(account="123456", password="123456a", email="a@gmail.com", name="n")

        self.assertEqual("123456", user.account)
        self.assertEqual("123456a", user.password.get_secret_value())
        self.assertEqual("a@gmail.com", user.email)
        self.assertEqual("n", user.name)
        self.assertIsNone(user.line_user_id)
