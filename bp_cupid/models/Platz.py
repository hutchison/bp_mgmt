"""
Ein Platz.
"""

from django.db import models
from bp_cupid.models import Student, Praxis, Zeitraum, Gewicht
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords

import logging
logger = logging.getLogger(__name__)


class Platz(models.Model):
    """
    Einem Platz sind ein Student, eine Praxis und ein Zeitraum zugeordnet.

    Dabei kann ein Platz nur einen Studenten enthalten (daher ist das der
    primary_key). Eine Praxis kann zu einem Zeitraum natürlich nur einen Platz
    haben (daher das unique_together).

    Dazu kommen die Attribute 'manuell' und 'kommentar'.
    """

    # Relationen
    student = models.OneToOneField(Student, primary_key=True, related_name='platz')
    praxis = models.ForeignKey(Praxis, related_name='plaetze')
    zeitraum = models.ForeignKey(Zeitraum, related_name='plaetze')

    # andere Attribute
    manuell = models.BooleanField(
        default=False,
        help_text="Wenn aktiviert, dann wird der Platz bei der automatischen\
        Platzvergabe nicht gelöscht.",
    )
    kommentar = models.TextField(
        default='',
        blank=True,
    )

    # Änderungsgeschichte:
    history = HistoricalRecords()


    def gewicht(self):
        """
        Gibt das Gewicht dieses Platzes zurück.
        """
        return Gewicht.objects.get(
            student=self.student,
            praxis=self.praxis,
        )

    @classmethod
    def vergib_platz(cls, s_id, p_id, z_id=None):
        """
        Vergibt einen Platz an den erstbesten Zeitraum an Studenten s_id und
        Praxis p_id.
        """
        student = Student.objects.get(id=s_id)
        praxis = Praxis.objects.get(id=p_id)
        if z_id:
            zeitraum = Zeitraum.objects.get(id=z_id)
        else:
            zeitraum = praxis.erster_freier_zeitraum()

        platz = cls(
            student=student,
            praxis=praxis,
            zeitraum=zeitraum,
            manuell=False
        )

        # Zur Sicherheit rufen wir vor dem Speichern nochmal full_clean() auf,
        # damit wir lieber eine Exception schmeißen als falsche Plätze zu
        # vergeben:

        platz.full_clean()
        logger.debug('Vergebe Platz: {}'.format(platz))
        platz.save()

        return platz

    def clean(self):
        verw_zr = self.zeitraum.block.verwaltungszeitraum
        if self.zeitraum not in self.praxis.zeitraeume.all():
            raise ValidationError(
                (
                    u'{praxis} bietet im Zeitraum {zeitraum} keinen Platz an. '
                    + u'Probiere folgende: {zeitraeume}'
                ).format(
                    praxis=self.praxis,
                    zeitraum=self.zeitraum,
                    zeitraeume=', '.join(
                        map(str, self.praxis.freie_zeitraeume.all())
                    )
                )
            )
        elif self.zeitraum not in self.praxis.freie_zeitraeume.all():
            raise ValidationError(
                (
                    u'Der Zeitraum {zeitraum} bei Praxis {praxis} ist ' +
                    u'schon belegt. Probiere folgende: {zeitraeume}'
                ).format(
                    praxis=self.praxis,
                    zeitraum=self.zeitraum,
                    zeitraeume=', '.join(
                        map(str, self.praxis.freie_zeitraeume.all())
                    )
                )
            )
        elif self.student.extern:
            raise ValidationError(
                u'Student absolviert das BP schon extern. ' +
                u'So kann kein Platz vergeben werden.'
            )
        elif self.praxis.platzbegrenzung.filter(
                verwaltungszeitraum=verw_zr
            ).exists():
            # Überprüfe die evtl. Platzbegrenzung
            pgrenze = self.praxis.platzbegrenzung.get(
                verwaltungszeitraum=verw_zr
            )
            anzahl_plaetze = self.praxis.plaetze.filter(
                zeitraum__block__verwaltungszeitraum=verw_zr,
            ).count()
            if pgrenze.anzahl <= anzahl_plaetze:
                raise ValidationError(
                    u'Maximale Platzgrenze ist erreicht.'
                )

    class Meta:
        verbose_name = 'Platz'
        verbose_name_plural = 'Plätze'
        unique_together = ('praxis', 'zeitraum')
        ordering = ['zeitraum']

    def __str__(self):
        man_text = 'manuell' if self.manuell else 'automatisch'
        return '{student} bei {praxis} in {zeitraum} ({manuell})'.format(
            student=self.student,
            praxis=self.praxis,
            zeitraum=self.zeitraum,
            manuell=man_text,
        )
