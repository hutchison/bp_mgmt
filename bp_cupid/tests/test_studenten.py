from django.test import TestCase
from bp_cupid.models import (
    Praxis,
    Zeitraum,
    Block,
    Verwaltungszeitraum,
    Student,
    Platz,
)
from datetime import date

class TestStudent(TestCase):
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

        self.st1 = Student.objects.get(pk=1)
        self.st2 = Student.objects.get(pk=2)

        self.pr1 = Praxis.objects.first()
        self.pr1.zeitraeume.all().delete()
        self.pr1.zeitraeume.add(self.zr1, self.zr2)
        self.pr1.save()

    def test_freie_studenten(self):
        """
        Alice und Bob müssten anfangs frei sein. Nach einer Platzzuweisung
        dürfte Alice nicht mehr frei sein.
        """
        self.assertIn(self.st1, Student.objects.frei())
        self.assertIn(self.st2, Student.objects.frei())

        Platz.vergib_platz(self.st1.id, self.pr1.id, self.zr1.id)

        self.assertNotIn(self.st1, Student.objects.frei())
        self.assertIn(self.st2, Student.objects.frei())

        self.st2.extern = True
        self.st2.save()

        self.assertNotIn(self.st1, Student.objects.frei())
        self.assertNotIn(self.st2, Student.objects.frei())
