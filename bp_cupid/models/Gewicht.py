"""
Ein Gewicht zwischen Student und Praxis.
"""

from django.db import models
from bp_cupid.models import (
    Student,
    Praxis,
)


class Gewicht(models.Model):
    """
    Ein Gewicht gibt an, wie gut ein Student und eine Praxis zusammenpassen. Je
    höher, desto besser.

    Der Wert an sich wird in 'wert' gespeichert. Dazu kommt ein Kommentar, der
    einem sagt, wie der Wert zustande gekommen ist.
    """
    # Relationen
    student = models.ForeignKey(Student, related_name='gewichte')
    praxis = models.ForeignKey(Praxis, related_name='gewichte')

    wert = models.FloatField()
    kommentar = models.TextField(
        default='',
        blank=True,
    )

    def umgebrochener_kommentar(self):
        """
        Gibt den Kommentar HTML-kompatibel zurück.
        """
        return '<br />'.join(self.kommentar.split('\n'))
    umgebrochener_kommentar.allow_tags = True
    umgebrochener_kommentar.short_description = 'Kommentar'

    @classmethod
    def berechne(cls, student=None, praxis=None):
        """
        Berechnet das Gewicht (den Score) zwischen einem Studenten und einer
        Praxis.
        """
        gewicht = 0.0
        kommentar = ''

        # Erstmal den inhaltlichen Teil:
        komm = '{wert:+} für {bezeichnung} (S will{will}, P hat{hat})\n'

        will = ''
        bezeichnung = 'Kinder'
        if praxis.kinder:
            hat = ''
            if student.gewichtung_kinder:
                if student.gewichtung_kinder == 2:
                    zuschlag = 5
                    will = ' sehr'
                else:
                    zuschlag = 2
            else:
                zuschlag = -2
                will = ' nicht'
        else:
            hat = ' nicht'
            if student.gewichtung_kinder:
                if student.gewichtung_kinder == 2:
                    zuschlag = -5
                    will = ' sehr'
                else:
                    zuschlag = -2
            else:
                zuschlag = 2
                will = ' nicht'

        gewicht += zuschlag
        kommentar += komm.format(
            wert=zuschlag,
            bezeichnung=bezeichnung,
            will=will,
            hat=hat,
        )

        will = ''
        bezeichnung = 'Sono'
        if praxis.sono:
            hat = ''
            if student.gewichtung_sono:
                if student.gewichtung_sono == 2:
                    zuschlag = 5
                    will = ' sehr'
                else:
                    zuschlag = 2
            else:
                zuschlag = -2
                will = ' nicht'
        else:
            hat = ' nicht'
            if student.gewichtung_sono:
                if student.gewichtung_sono == 2:
                    zuschlag = -5
                    will = ' sehr'
                else:
                    zuschlag = -2
            else:
                zuschlag = 2
                will = ' nicht'

        gewicht += zuschlag
        kommentar += komm.format(
            wert=zuschlag,
            bezeichnung=bezeichnung,
            will=will,
            hat=hat,
        )

        will = ''
        bezeichnung = 'Sport'
        if praxis.sport:
            hat = ''
            if student.gewichtung_sport:
                if student.gewichtung_sport == 2:
                    zuschlag = 5
                    will = ' sehr'
                else:
                    zuschlag = 2
            else:
                zuschlag = -2
                will = ' nicht'
        else:
            hat = ' nicht'
            if student.gewichtung_sport:
                if student.gewichtung_sport == 2:
                    zuschlag = -5
                    will = ' sehr'
                else:
                    zuschlag = -2
            else:
                zuschlag = 2
                will = ' nicht'

        gewicht += zuschlag
        kommentar += komm.format(
            wert=zuschlag,
            bezeichnung=bezeichnung,
            will=will,
            hat=hat,
        )

        will = ''
        bezeichnung = 'Komplementärmed.'
        if praxis.kompl:
            hat = ''
            if student.gewichtung_kompl:
                if student.gewichtung_kompl == 2:
                    zuschlag = 5
                    will = ' sehr'
                else:
                    zuschlag = 2
            else:
                zuschlag = -10
                will = ' nicht'
        else:
            hat = ' nicht'
            if student.gewichtung_kompl:
                if student.gewichtung_kompl == 2:
                    zuschlag = -5
                    will = ' sehr'
                else:
                    zuschlag = -2
            else:
                zuschlag = 2
                will = ' nicht'

        gewicht += zuschlag
        kommentar += komm.format(
            wert=zuschlag,
            bezeichnung=bezeichnung,
            will=will,
            hat=hat,
        )

        # Bonus für die Bundeswehr:
        komm = '{wert:+} für Bundeswehr ({interesse} Interesse)\n'
        interesse = ''
        if praxis.id in [40, 75]:
            if student.gewichtung_hohe_duene:
                if student.gewichtung_hohe_duene == 2:
                    zuschlag = 5
                    interesse = 'großes'
                else:
                    zuschlag = 2
                    interesse = 'etwas'
            else:
                zuschlag = -10
                interesse = 'kein'

            gewicht += zuschlag
            kommentar += komm.format(
                wert=zuschlag,
                interesse=interesse,
            )

        # Boni für Landkreis:
        if student.anzahl_landkreise() == 3:
            landkr = praxis.landkreis
            if landkr in student.landkreise.all():
                zuschlag = 3
                gewicht += zuschlag
                kommentar += '+{} für Landkreis {}\n'.format(zuschlag, landkr)

        # Bonus für freie Unterkunft bzw. besondere Praxis:
        if praxis in student.bevorzugte_praxen.all():
            zuschlag = 7
            gewicht += zuschlag
            kommentar += '+{} für besondere Praxis\n'.format(zuschlag)

        # Bonuspunkte, wenn der Student ein Auto hat.
        if student.fs_und_fahrzeug:
            if praxis.nur_mit_auto:
                if praxis not in student.bevorzugte_praxen.all():
                    zuschlag = 7
                    gewicht += zuschlag
                    kommentar += '+{} für Erreichbarkeit (S hat FS und Auto)'.format(zuschlag)
        else:
            if praxis.nur_mit_auto:
                if praxis not in student.bevorzugte_praxen.all():
                    zuschlag = -50
                    gewicht += zuschlag
                    kommentar += '{} für Erreichbarkeit (per pedes)'.format(zuschlag)

        return cls(
            student=student,
            praxis=praxis,
            wert=gewicht,
            kommentar=kommentar
        )

    class Meta:
        verbose_name = 'Gewicht'
        verbose_name_plural = 'Gewichte'
        unique_together = ('student', 'praxis')

    def __str__(self):
        return '%s %s: %.3f' % (self.student, self.praxis, self.wert)
