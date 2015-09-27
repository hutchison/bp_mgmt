from django.test import TestCase
from django.contrib.auth.models import User


class PreexistingUsersTestCase(TestCase):
    def test_preexisting_users(self):
        """
        Existieren die Benutzer aus pree_users?
        """
        pree_users = ['admin', 'amueller', 'annette', 'anne', 'beate']
        for uname in pree_users:
            self.assertTrue(User.objects.filter(username=uname).exists())
