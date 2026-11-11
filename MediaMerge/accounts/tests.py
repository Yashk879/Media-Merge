from django.test import TestCase
from django.contrib.auth.models import User

class AccountTests(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username="demo", password="password123")
        self.assertTrue(user.check_password("password123"))
