from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver

from .models import (
    Platz,
    Praxis,
    Student,
    Zeitraum,
)
from .tasks import (
    berechne_gewichte_von_praxis,
    berechne_gewichte_von_student,
)

import logging
logger = logging.getLogger(__name__)


@receiver(post_save, sender=Praxis)
def aktualisiere_zeitraeume_nach_praxisspeicherung(sender, instance, **kwargs):
    """
    Wir können die Zeiträume erst aktualisieren, wenn die Praxis in der
    Datenbank gespeichert wurde (und damit eine id hat):
    """
    logger.debug(
        'Aktualisiere Zeiträume von {}.'.format(instance)
    )
    instance.aktualisiere_zeitraeume()

"""
Hier aktualisieren wir die Zeiträume einer Praxis immer dann, wenn die
ManyToMany-Beziehung Praxis-Zeitraum geändert wird:
"""
m2m_changed.connect(
    aktualisiere_zeitraeume_nach_praxisspeicherung,
    sender=Praxis.zeitraeume.through,
)


@receiver(post_save, sender=Praxis)
def aktualisiere_gewichte_nach_praxisspeicherung(sender, instance, **kwargs):
    logger.debug('Berechne Gewichte von {}.'.format(instance))
    berechne_gewichte_von_praxis.delay(instance.id)


@receiver(post_save, sender=Student)
def aktualisiere_gewichte_nach_studentenspeicherung(sender, instance, **kwargs):
    logger.debug('Berechne Gewichte von {}.'.format(instance))
    berechne_gewichte_von_student.delay(instance.id)


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


@receiver(post_save, sender=Zeitraum)
def aktualisiere_ueberlappende_zeitraeume(sender, instance, **kwargs):
    instance.aktualisiere_zeitraeume()
    logger.debug('Aktualisiere überlappende Zeiträume von {}'.format(instance))
