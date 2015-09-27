"""
Zusatzinfo an eine Praxis.
"""

from django.db import models
from bp_cupid.models import (
    Praxis,
    Verwaltungszeitraum,
)
from simple_history.models import HistoricalRecords


class ZusatzinfoPraxis(models.Model):
    praxis = models.ForeignKey(Praxis)
    verwaltungszeitraum = models.ForeignKey(Verwaltungszeitraum)
    text = models.TextField(
        default='',
        blank=True,
        help_text=('Einfache HTML-Tags wie &lt;b&gt;, &lt;i&gt; und &lt;u&gt;'
        'funktionieren. Von weiteren Experimenten sollte man ablassen.'),
    )
    # Änderungsgeschichte:
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Zusatzinfo an Praxis'
        verbose_name_plural = 'Zusatzinfos an Praxen'
        unique_together = ('praxis', 'verwaltungszeitraum')

    def __str__(self):
        return '<{}: {} in {}: {}>'.format(
            self.__class__.__name__,
            self.praxis.name,
            self.verwaltungszeitraum.name,
            self.text,
        )
