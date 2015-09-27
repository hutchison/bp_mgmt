from django.test import TestCase
from bp_cupid.models import Praxis, Zeitraum, Block

class TestPraxis(TestCase):
    fixtures = [
        'testdata/verwaltungszeitraum_testdata',
        'testdata/block_testdata',
        'testdata/zeitraum_testdata',
        'testdata/student_testdata',
        'testdata/praxis_testdata',
    ]

    def setUp(self):
        self.block1 = Block.objects.first()
        zr1 = Zeitraum.objects.get(pk=1)
        zr2 = Zeitraum.objects.get(pk=2)
        self.pr1 = Praxis.objects.first()
        self.pr1.zeitraeume.all().delete()
        self.pr1.zeitraeume.add(zr1, zr2)

    def test_kapazitaet(self):
        """
        Die Praxis bietet 2 Zeiträume an, die sich jedoch überlagern. Also
        müsste die Kapazität vom ersten Block 1 betragen.
        """
        self.assertEqual(
            self.pr1.kapazitaet(self.block1),
            1
        )

    def test_maximale_kapazitaet(self):
        """
        Die Praxis bietet 2 Zeiträume an, die sich jedoch überlagern. Also
        müsste die maximale Kapazität 1 betragen.
        """
        self.assertEqual(
            self.pr1.maximale_kapazitaet(),
            1
        )
