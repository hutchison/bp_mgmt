from django.test import TestCase
from bp_cupid.models import Verwaltungszeitraum


class PreexistingVerwaltungszeitraumeTestCase(TestCase):
    def test_preexisting_verwaltungszeitraume(self):
        """
        Existiert der schon vorhandene Verwaltungszeitraum?
        """
        self.assertTrue(
            Verwaltungszeitraum.objects.filter(name='WS1415-SS15').exists()
        )
