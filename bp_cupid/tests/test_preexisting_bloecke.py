from django.test import TestCase
from bp_cupid.models import Block


class PreexistingBlocksTestCase(TestCase):
    def test_preexisting_bloecke(self):
        """
        Existieren die Blöcke aus den fixtures?
        """
        for i in range(1, 9):
            self.assertTrue(
                Block.objects.filter(
                    name='Block %i' % i
                ).exists()
            )
