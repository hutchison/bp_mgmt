"""
Testet die Platzbegrenzungen.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from bp_cupid.models import (
    Student,
    Verwaltungszeitraum,
    Praxis,
    Platzbegrenzung,
    Platz,
)

class TestPlatzbegrenzungen(TestCase):
    """
    Testet die Platzbegrenzungen.
    """
    fixtures = [
        'testdata/verwaltungszeitraum_testdata',
        'testdata/block_testdata',
        'testdata/zeitraum_testdata',
        'testdata/praxis_testdata',
        'testdata/student_testdata',
    ]

    def setUp(self):
        # Hier müssen wir erst alle Plätze löschen, weil er sonst mit den
        # fixtures aus den Migrationen durcheinanderkommt und annimmt, dass die
        # meisten Studenten schon einen Platz hätten:
        Platz.objects.all().delete()

        self.st1 = Student.objects.get(pk=1)
        self.st2 = Student.objects.get(pk=2)
        self.verwzr = Verwaltungszeitraum.objects.first()

        # Suche die erste Praxis, die auch was anzubieten hat:
        for praxis in Praxis.objects.all():
            if praxis.maximale_kapazitaet():
                self.pr1 = praxis
                break

    def test_keine_plaetze_vergeben(self):
        """
        Wenn eine Praxis keine Studenten will, obwohl sie Zeiträume anbietet,
        dann soll sie keine bekommen.
        """
        Platzbegrenzung.objects.create(
            verwaltungszeitraum=self.verwzr,
            praxis=self.pr1,
            anzahl=0,
        )

        with self.assertRaisesRegex(ValidationError, 'Maximale Platzgrenze ist erreicht.'):
            Platz.vergib_platz(self.st1.id, self.pr1.id)

    def test_einen_platz_vergeben(self):
        """
        Wenn eine Praxis nur einen Studenten will, dann soll beim Versuch einen
        zweiten zuzuweisen eine Exception geworfen werden.
        """
        Platzbegrenzung.objects.create(
            verwaltungszeitraum=self.verwzr,
            praxis=self.pr1,
            anzahl=1,
        )
        Platz.vergib_platz(self.st1.id, self.pr1.id)

        with self.assertRaisesRegex(ValidationError, 'Maximale Platzgrenze ist erreicht.'):
            Platz.vergib_platz(self.st2.id, self.pr1.id)

    def test_negative_anzahl(self):
        """
        Die Anzahl darf nicht negativ sein. Falls doch, sollte ein
        ValidationError geworfen werden.
        """
        platzgrenze = Platzbegrenzung.objects.create(
            verwaltungszeitraum=self.verwzr,
            praxis=self.pr1,
            anzahl=-1,
        )
        with self.assertRaisesRegex(ValidationError, 'Anzahl darf nicht negativ sein.'):
            platzgrenze.full_clean()
