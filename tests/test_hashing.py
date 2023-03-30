from unittest import TestCase

from app.user.hashing import get_password_hash, verify_password


class Test(TestCase):
    def test_password_gen(self):
        plain = "mypwd"
        hashed = get_password_hash(plain)
        self.assertTrue(verify_password(plain, hashed))
