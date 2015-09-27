from django.test import TestCase
from bp_cupid.models import Praxis


class TestPreexistingPraxen(TestCase):
    def setUp(self):
        self.praxen = Praxis.objects.all()

    def test_sind_alle_praxen_in_ordnung(self):
        """
        Hier testen wir, ob alle bisher verteilten Plätze konsistent sind.

        Dazu darf der Zeitraum eines Platzes nicht mit den anderen überlappen.
        """
        for praxis in self.praxen:
            for platz in praxis.plaetze.order_by('zeitraum__anfang'):
                andere_plaetze = praxis.plaetze.exclude(pk=platz.pk)
                ueberlappende_zrs = platz.zeitraum.ueberlappende_zeitraeume()

                for and_platz in andere_plaetze:
                    self.assertNotIn(
                        and_platz.zeitraum,
                        ueberlappende_zrs
                    )
