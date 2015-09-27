"""
Die Klasse der Textvorlagen für E-Mails etc.
"""

from django.db import models

class Vorlage(models.Model):
    """
    Hier werden alle angezeigten Texte gespeichert, damit sie nicht fest in den
    Code gepresst sind.
    """
    token = models.SlugField(
        unique=True,
        null=False,
        blank=False,
        help_text='Das Kürzel, über das die Vorlage im Code angesprochen wird.'
    )
    text = models.TextField(
        null=False,
        blank=True,
        default='',
        help_text="""Der eigentliche Text der Vorlage, der angezeigt wird."""
    )

    class Meta:
        verbose_name = 'Vorlage'
        verbose_name_plural = 'Vorlagen'

    def __str__(self):
        return self.token
