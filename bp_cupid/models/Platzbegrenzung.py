"""
Eine Platzbegrenzung.
"""

from django.db import models
from django.core.validators import MinValueValidator
from bp_cupid.models import (
    Praxis,
    Verwaltungszeitraum,
)


class Platzbegrenzung(models.Model):
    """
    Eine Platzbegrenzung gibt an, wieviele Plätze eine Praxis in einem
    Verwaltungszeitraum maximal haben möchte.

    Durch die Fremdschlüssel haben wir den Vorteil, dass das Nichtvorhandensein
    einer Begrenzung durch das Nichtvorhandensein der Relation gelöst wird.
    """
    verwaltungszeitraum = models.ForeignKey(
        Verwaltungszeitraum,
        related_name='platzbegrenzung',
    )
    praxis = models.ForeignKey(
        Praxis,
        related_name='platzbegrenzung',
    )
    anzahl = models.IntegerField(
        verbose_name='max. Anzahl Plätze',
        validators=[MinValueValidator(0, 'Anzahl darf nicht negativ sein.')],
    )

    class Meta:
        verbose_name = 'Platzbegrenzung'
        verbose_name_plural = 'Platzbegrenzungen'
        unique_together = ('verwaltungszeitraum', 'praxis')

    def __str__(self):
        return 'maximal {anzahl} Plätze für {praxis} in {verwzr}'.format(
            praxis=self.praxis,
            verwzr=self.verwaltungszeitraum,
            anzahl=self.anzahl,
        )
