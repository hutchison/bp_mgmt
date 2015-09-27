from django.test import TestCase
from bp_cupid.models import Zeitraum

class TestZeitraum(TestCase):
    fixtures = [
        'testdata/verwaltungszeitraum_testdata',
        'testdata/block_testdata',
        'testdata/zeitraum_testdata',
    ]

    def setUp(self):
        self.zr1 = Zeitraum.objects.get(pk=1)
        self.zr2 = Zeitraum.objects.get(pk=2)

    def test_zeitraum(self):
        self.assertIn(
            self.zr1,
            self.zr1.ueberlappende_zeitraeume()
        )
        self.assertIn(
            self.zr2,
            self.zr1.ueberlappende_zeitraeume()
        )
        self.assertIn(
            self.zr1,
            self.zr2.ueberlappende_zeitraeume()
        )
        self.assertIn(
            self.zr2,
            self.zr2.ueberlappende_zeitraeume()
        )
