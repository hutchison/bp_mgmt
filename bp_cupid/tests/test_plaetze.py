"""
Testet die Funktionen von Platz.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from bp_cupid.models import (
    Praxis,
    Zeitraum,
    Block,
    Platz,
    Student,
)

class TestPlatz(TestCase):
    fixtures = [
        'testdata/verwaltungszeitraum_testdata',
        'testdata/block_testdata',
        'testdata/zeitraum_testdata',
        'testdata/student_testdata',
        'testdata/praxis_testdata',
    ]

    def setUp(self):
        # Erst alle Plätze löschen, sonst kommen wir mit den schon vorhandenen
        # durcheinander:
        Platz.objects.all().delete()

        self.block1 = Block.objects.first()
        self.zr1 = Zeitraum.objects.get(pk=1)
        self.zr2 = Zeitraum.objects.get(pk=2)
        self.zr3 = Zeitraum.objects.get(pk=3)

        self.st1 = Student.objects.get(pk=1)
        self.st2 = Student.objects.get(pk=2)

        self.pr1 = Praxis.objects.first()
        # Hier passen wir die Testdaten der Situation ein bisschen an. Die
        # Praxis soll nur die ersten beiden Zeiträume anbieten:
        self.pr1.zeitraeume.all().delete()
        self.pr1.zeitraeume.add(self.zr1, self.zr2)
        self.pr1.save()

    def test_nur_ein_student_pro_zeitraum(self):
        """
        Pro Praxis und Zeitraum kann nur ein Student eingeteilt werden.

        Hier versuchen wir zwei Studenten zu einer Praxis in einem Zeitraum
        zuzuordnen.
        """
        Platz.vergib_platz(self.st1.id, self.pr1.id, self.zr1.id)
        with self.assertRaises(ValidationError):
            Platz.vergib_platz(self.st2.id, self.pr1.id, self.zr1.id)

    def test_keine_ueberlappenden_zeitraeume(self):
        """
        Falls ein Zeitraum von einem Studenten belegt ist und ein anderer
        Zeitraum mit diesem überlappt, dann kann letzterer nicht belegt werden.

        Hier vergeben wir den ersten Zeitraum an Alice. Wenn wir versuchen, den
        zweiten Zeitraum an Bob zu vergeben, müsste eine Exception geworfen
        werden.
        """
        Platz.vergib_platz(self.st1.id, self.pr1.id, self.zr1.id)
        with self.assertRaises(ValidationError):
            Platz.vergib_platz(self.st2.id, self.pr1.id, self.zr2.id)

    def test_zeitraum_wird_nicht_angeboten(self):
        """
        Falls eine Praxis den Zeitraum gar nicht erst anbietet, müsste eine
        Exception geworfen werden.
        """
        with self.assertRaises(ValidationError):
            Platz.vergib_platz(self.st1.id, self.pr1.id, self.zr3.id)

    def test_praxis_voll_belegt(self):
        """
        Wenn wir einen Zeitraum der Praxis belegen, müsste sie voll belegt sein.
        Davor nicht.
        """
        self.assertFalse(self.pr1.voll_belegt())
        Platz.vergib_platz(self.st1.id, self.pr1.id, self.zr1.id)
        self.assertTrue(self.pr1.voll_belegt())

    def test_freie_zeitraeume_in_block(self):
        """
        Zu Beginn müsste unsere Praxis die beiden Zeiträume 1 und 2 als 'frei'
        erachten. Wenn wir danach einen Platz vergeben, müsste sie keine freien
        Plätze mehr haben.
        """
        self.assertEqual(
            self.pr1.freie_zeitraeume_in_block(self.block1),
            [self.zr1, self.zr2]
        )
        self.assertTrue(self.pr1.hat_platz_in_block(self.block1))

        Platz.vergib_platz(self.st1.id, self.pr1.id)

        self.assertEqual(
            self.pr1.freie_zeitraeume_in_block(self.block1),
            []
        )
        self.assertFalse(self.pr1.hat_platz_in_block(self.block1))
