from celery import shared_task
from django.core.cache import cache

from .models import (
    Gewicht,
    Praxis,
    Block,
    Student,
    Platz,
    Zeitraum,
    Platzbegrenzung,
)

import logging
logger = logging.getLogger(__name__)

LOCK_EXPIRE = 60 * 5
BERECHNE_GEWICHTE_LOCK_ID = 'berechne_gewichte_lock'
VERTEILE_PLAETZE_LOCK_ID = 'verteile_plaetze_lock'


@shared_task
def berechne_gewichte(verwaltungszeitraum_id):
    """
    Berechnet alle Gewichte (Scores) zwischen Studenten und Praxen.
    """

    if cache.add(BERECHNE_GEWICHTE_LOCK_ID, True, LOCK_EXPIRE):
        try:
            Gewicht.objects.all().delete()

            praxen = Praxis.objects.all()
            studenten = Student.objects.filter(
                verwaltungszeitraum_id=verwaltungszeitraum_id
            )

            gs = (Gewicht.berechne(s, p) for s in studenten for p in praxen)
            Gewicht.objects.bulk_create(gs)
        finally:
            cache.delete(BERECHNE_GEWICHTE_LOCK_ID)


@shared_task
def berechne_gewichte_von_praxis(praxis_id):
    """
    Berechnet die Gewichte einer Praxis und allen Studenten.
    """
    praxis = Praxis.objects.get(id=praxis_id)
    studenten = Student.objects.all()

    Gewicht.objects.filter(praxis=praxis).delete()

    gs = (Gewicht.berechne(s, praxis) for s in studenten)
    Gewicht.objects.bulk_create(gs)


@shared_task
def berechne_gewichte_von_student(student_id):
    """
    Berechnet die Gewichte eines Studenten und allen Praxen.
    """
    student = Student.objects.get(id=student_id)
    praxen = Praxis.objects.all()

    Gewicht.objects.filter(student=student).delete()

    gs = (Gewicht.berechne(student, p) for p in praxen)
    Gewicht.objects.bulk_create(gs)


@shared_task
def verteile_studenten_task(anzahl=120, blocklimit=30, bloecke=None, loeschen=False):
    if cache.add(VERTEILE_PLAETZE_LOCK_ID, True, LOCK_EXPIRE):
        try:
            gewaehlte_bloecke = Block.objects.filter(id__in=bloecke)
            verw_zr = gewaehlte_bloecke.first().verwaltungszeitraum

            if loeschen:
                loesche_alle_plaetze(verw_zr)
            verteile_studenten(anzahl, blocklimit, gewaehlte_bloecke)
        finally:
            cache.delete(VERTEILE_PLAETZE_LOCK_ID)


def verteile_studenten(anzahl=120, blocklimit=30, bloecke=None):
    """
    Nimmt zufällig 'anzahl' freie Studenten, die den Fragebogen ausgefüllt
    haben, und verteilt sie auf die übergebenen Blöcke.
    """

    verw_zr = bloecke.first().verwaltungszeitraum
    gewaehlte_zeitraeume = Zeitraum.objects.filter(block__in=bloecke)
    studenten = Student.objects.frei().filter(
        hat_fragebogen_ausgefuellt=True,
        verwaltungszeitraum=verw_zr,
    ).prefetch_related(
        'gewichte'
    ).order_by('?')[:int(anzahl)]

    logger.debug('Starte Verteilung der Studenten')
    logger.debug(
        'Anzahl: {}, Blocklimit: {}, Blöcke: {}'.format(
            anzahl, blocklimit, bloecke,
        )
    )

    """
    Wir gehen die zufällig ausgesuchten Studenten der Reihe nach durch:
    """
    for s in studenten:
        if s.extern:
            logger.debug('{} macht BP extern. Wird übersprungen.'.format(s))
            continue

        logger.debug('Verteile {}'.format(s))
        """
        Bei einem Studenten gehen wir die Gewichte vom höchsten zum niedrigsten
        durch:
        """
        gewichte = s.sortierte_gewichte()
        for g in gewichte:
            praxis = g.praxis

            """
            Überprüfe die Platzbegrenzung; wenn das Limit der Praxis erreicht
            ist, gehe zur nächsten:
            """
            try:
                pg = praxis.platzbegrenzung.get(verwaltungszeitraum=verw_zr)
                anzahl_plaetze = praxis.plaetze.filter(
                    zeitraum__block__verwaltungszeitraum=verw_zr,
                ).count()
                if anzahl_plaetze >= pg.anzahl:
                    logger.debug(
                        'Platzbegrenzung: '
                        'das Limit von {} der Praxis {} ist erreicht.'.format(
                            pg.anzahl,
                            praxis,
                        )
                    )
                    continue
            except Platzbegrenzung.DoesNotExist:
                pass

            for z in praxis.freie_zeitraeume.all():
                """
                Wenn die Praxis in den Zeiträumen des Blocks noch einen freien
                Zeitraum hat und das Blocklimit noch nicht erreicht ist, dann
                wird der Platz vergeben:
                """
                if (
                        z in gewaehlte_zeitraeume
                        and z.block in bloecke
                        and z.block.anzahl_plaetze() < int(blocklimit)
                    ):
                    Platz.vergib_platz(s.id, praxis.id, z.id)
                    break
            """
            Falls ein Platz vergeben wurde, brechen wir aus und gehen zum
            nächsten Studenten:
            """
            if Platz.objects.filter(student=s):
                break

    logger.debug('Verteilung der Studenten beendet')


def loesche_alle_plaetze(verwaltungszeitraum):
    """
    Löscht alle automatisch vergebenen Plätze des übergebenen
    Verwaltungszeitraums
    """
    logger.debug(
        'Lösche alle automatisch vergebenen Plätze '
        'des Verwaltungszeitraums {}'.format(verwaltungszeitraum)
    )
    Platz.objects.filter(
        manuell=False,
        student__verwaltungszeitraum=verwaltungszeitraum,
    ).delete()
    logger.debug('Plätze gelöscht')
