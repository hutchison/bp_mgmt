"""
Ein Block.
"""

from django.db import models
from bp_cupid.models import Verwaltungszeitraum
from operator import attrgetter


class Block(models.Model):
    """
    Ein Block ist immer einem Verwaltungszeitraum zugeordnet und hat einen
    Namen. Der Name muss nicht eindeutig sein, da ja in jedem
    Verwaltungszeitraum die Blöcke wieder von 1 bis n durchnummeriert werden.

    Dafür müssen Name + Verwaltungszeitraum eindeutig sein (siehe Meta).
    """
    verwaltungszeitraum = models.ForeignKey(
        Verwaltungszeitraum,
        related_name='bloecke',
    )
    name = models.CharField(max_length=20)

    def zeiten(self):
        """
        Macht die Zeiträume für die Adminseiten zurecht und gibt sie zurück.
        """
        return '<br />'.join(map(str, self.zeitraeume.all()))
    zeiten.allow_tags = True
    zeiten.short_description = 'Zeiträume'

    def anzahl_plaetze(self):
        """
        Gibt die Anzahl aller Plätze des Blocks zurück.
        """
        return sum(z.plaetze.count() for z in self.zeitraeume.all())

    def maximale_kapazitaet(self):
        """
        Gibt die maximale Kapazität des Blocks zurück.

        Dazu gehen wir alle Praxen durch und summieren die Kapazitäten für
        diesen Block.
        """
        praxen = set()
        for z in self.zeitraeume.prefetch_related('praxen__zeitraeume'):
            praxen.update((p for p in z.praxen.all()))

        return sum(p.kapazitaet(self) for p in praxen)

    def anzahl_freie_plaetze(self):
        """
        Gibt die Anzahl freier Plätze des Blocks zurück.
        """
        return self.maximale_kapazitaet() - self.anzahl_plaetze()

    def plaetze(self):
        """
        Gibt alle Plätze dieses Blocks zurück.
        """
        platzliste = []
        for zeitraum in self.zeitraeume.prefetch_related('plaetze__student'):
            platzliste.extend(
                sorted(
                    zeitraum.plaetze.all(),
                    key=attrgetter('student.name'),
                )
            )
        return platzliste

    class Meta:
        verbose_name = 'Block'
        verbose_name_plural = 'Blöcke'
        unique_together = ('name', 'verwaltungszeitraum')

    def __str__(self):
        return '{} ({})'.format(self.name, self.verwaltungszeitraum)
