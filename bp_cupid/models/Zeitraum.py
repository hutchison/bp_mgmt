"""
Ein Zeitraum.
"""

from django.db import models
from django.db.models import Q
from bp_cupid.models import Block


class Zeitraum(models.Model):
    """
    Ein Zeitraum ist einem Block zugeordnet. Er hat ein Anfang und ein Ende.
    """
    block = models.ForeignKey(
        Block,
        related_name='zeitraeume'
    )
    ueberlappende = models.ManyToManyField(
        'self',
        related_name='ueberlappende_zrs',
        related_query_name='ueberlappende',
        db_table='ueberlappende_zeitraeume',
        symmetrical=True,
        blank=True,
    )

    anfang = models.DateField()
    ende = models.DateField()

    def ueberlappende_zeitraeume(self):
        """
        Gibt alle Zeiträume zurück, die sich mit diesem hier überlappen.
        """
        return Zeitraum.objects.filter(
            Q(anfang__gte=self.anfang, anfang__lte=self.ende)
            | Q(anfang__lte=self.anfang, ende__gte=self.anfang)
        )

    def aktualisiere_zeitraeume(self):
        """
        Löscht alle überlappenden Zeiträume und berechnet sie dann neu.
        """
        for zr in self.ueberlappende.all():
            self.ueberlappende.remove(zr)

        for zr in self.ueberlappende_zeitraeume():
            self.ueberlappende.add(zr)

    class Meta:
        verbose_name = 'Zeitraum'
        verbose_name_plural = 'Zeiträume'
        ordering = ['anfang']

    def __str__(self):
        return '%s - %s (%s)' % (self.anfang, self.ende, self.id)
