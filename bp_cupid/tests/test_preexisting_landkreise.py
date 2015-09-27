from django.test import TestCase
from bp_cupid.models import Landkreis


class PreexistingLandkreiseTestCase(TestCase):
    def test_preexisting_landkreise(self):
        """
        Existieren die schon vorhandenen Landkreise?
        """
        plzs = [
            (17160, 17179),
            (18000, 18198),
            (18200, 18239),
            (18240, 18258),
            (18260, 18299),
            (18300, 18348),
            (19000, 19101),
            (19220, 19249),
            (19380, 19399),
            (23950, 23999),
        ]
        for plz in plzs:
            self.assertTrue(
                Landkreis.objects.filter(
                    plz_von=plz[0],
                    plz_bis=plz[1]
                ).exists()
            )

    def test_number_of_preexisting_landkreise(self):
        """
        Gibt es wirklich nur 10 Landkreise? Wenn nicht, läuft irgendwas falsch.
        """
        self.assertEqual(
            Landkreis.objects.count(),
            10
        )
