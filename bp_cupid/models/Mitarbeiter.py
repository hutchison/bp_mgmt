"""
Zusätzliche Informationen für Mitarbeiter.
"""

from django.db import models
from django.conf import settings
from bp_cupid.models import Verwaltungszeitraum

class Mitarbeiter(models.Model):
    """
    Um Informationen wie den aktuell eingestellten Verwaltungszeitraum zu
    speichern, müssen wir eine Proxyklasse zu User erstellen, in der wir die
    zusätzlichen Infos ablegen. Siehe dazu
    https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#extending-the-existing-user-model
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
    )
    akt_verw_zeitraum = models.ForeignKey(
        Verwaltungszeitraum,
        default=1,
        verbose_name='aktueller Verwaltungszeitraum',
        help_text=(u'Bei allen Ansichten werden nur Blöcke und Zeiträume des '
        u'aktuellen Verwaltungszeitraums angezeigt.')
    )

    class Meta:
        verbose_name = 'Mitarbeiter'
        verbose_name_plural = 'Mitarbeiter'

    def __str__(self):
        return self.user.get_full_name()
