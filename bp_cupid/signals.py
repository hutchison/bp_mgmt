from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from bp_cupid.models import (
    Praxis,
    Platz,
)

import logging
logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Praxis)
def aktualisiere_zeitraeume_vor_praxisspeicherung(sender, instance, **kwargs):
    # Wir können die Zeiträume erst aktualisieren, wenn die Praxis in der
    # Datenbank gespeichert wurde (und damit eine id hat):
    if instance.id:
        logger.debug(
            'Signal pre_save von Praxis erhalten. '
            'Aktualisiere Zeiträume von {}.'.format(instance)
        )
        instance.aktualisiere_zeitraeume()

@receiver(post_save, sender=Platz)
def aktualisiere_zeitraeume_nach_platzspeicherung(sender, instance, **kwargs):
    praxis = instance.praxis
    logger.debug(
        'Signal post_save von Platz erhalten. '
        'Aktualisiere Zeiträume von {}.'.format(praxis)
    )
    praxis.aktualisiere_zeitraeume()

@receiver(post_delete, sender=Platz)
def aktualisiere_zeitraeume_nach_platzloeschung(sender, instance, **kwargs):
    praxis = instance.praxis
    praxis.aktualisiere_zeitraeume()
    logger.debug(
        'Signal post_delete von Platz erhalten. '
        'Aktualisiere Zeiträume von {}.'.format(praxis)
    )
