from django.shortcuts import render
from django.core.cache import cache
from django.contrib.auth.decorators import login_required, user_passes_test
from actstream import action
from bp_cupid.tasks import verteile_studenten_task, VERTEILE_PLAETZE_LOCK_ID
from bp_cupid.models import (
    Student,
    Block,
    Platz,
)
from random import choice

import logging
logger = logging.getLogger(__name__)


@login_required
@user_passes_test(lambda u: u.is_staff)
def zufaellig_verteilen(request):
    """
    View für die zufällige Verteilung von Studenten an Praxen.
    """
    akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum
    bloecke = akt_verw_zr.bloecke.order_by('name').prefetch_related(
        'zeitraeume__plaetze',
    )
    freie_studenten = Student.objects.frei().filter(
        verwaltungszeitraum=akt_verw_zr,
    )

    context = {
        'bloecke': bloecke,
        'anzahl_freie_studenten': freie_studenten.count(),
    }

    if request.method == 'POST':
        if not cache.get(VERTEILE_PLAETZE_LOCK_ID):
            gewaehlte_bloecke = [int(b) for b in request.POST.getlist('block')]
            anzahl_studenten = request.POST.get('anzahl_studenten')
            blocklimit = request.POST.get('blocklimit')

            loeschen = bool(request.POST.get('loeschen', False))

            result = verteile_studenten_task.delay(
                anzahl_studenten,
                blocklimit,
                gewaehlte_bloecke,
                loeschen,
            )
            action.send(
                request.user,
                verb='startete Platzverteilung'
            )
            context['laufende_Platzverteilung'] = True

    if cache.get(VERTEILE_PLAETZE_LOCK_ID):
        context['laufende_Platzverteilung'] = True

    return render(request, 'bp_cupid/zufaellig_verteilen.html', context)


def verteile_studenten_auf_block(studenten, block):
    studenten = list(studenten)
    logger.debug(
        "Verteile die Studenten {} auf Block {}".format(
            studenten,
            block
        )
    )
    plaetze = []

    """
    TODO: das muss ich mal überarbeiten.
    Wir prüfen hier, ob ein Student Gewichte hat. Eigentlich sollten wir
    sicherstellen, dass immer alle Gewichte vorhanden sind, oder aber die
    Gewichte berechnen, wenn wir sie brauchen.
    """
    while studenten:
        student = choice(studenten)
        logger.debug("Versuche Student {} zu verteilen".format(student))
        logger.debug("dieser hat {} Gewichte".format(student.gewichte.count()))

        if student.gewichte.exists():
            for gewicht in student.gewichte.order_by('-wert'):
                praxis = gewicht.praxis
                if praxis.hat_platz_in_block(block):
                    zeitraum = praxis.freie_zeitraeume_in_block(block)[0]
                    platz = Platz.vergib_platz(
                        student.id,
                        praxis.id,
                        zeitraum.id
                    )
                    student.verwaltungszeitraum = block.verwaltungszeitraum
                    student.save()
                    plaetze.append(platz)
                    studenten.remove(student)
                    break
        else:
            logger.debug(
                "Überspringe Student {}, weil keine Gewichte vorhanden sind.".format(
                    student
                )
            )
            studenten.remove(student)

    return plaetze


@login_required
@user_passes_test(lambda u: u.is_staff)
def gezielt_verteilen(request):
    akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum
    context = dict()

    if request.method == 'POST':
        block_id = int(request.POST.get('block'))
        block = Block.objects.get(id=block_id)
        mat_nrs = map(int, request.POST.getlist('student'))
        studenten = Student.objects.filter(mat_nr__in=mat_nrs)
        plaetze = []

        plaetze = verteile_studenten_auf_block(studenten, block)

        context['plaetze'] = plaetze

    freie_studenten = Student.objects.frei().order_by('name')
    bloecke = akt_verw_zr.bloecke.order_by('name').prefetch_related(
        'zeitraeume__plaetze',
    )

    context['freie_studenten'] = freie_studenten
    context['bloecke'] = bloecke

    return render(request, 'bp_cupid/gezielt_verteilen.html', context)
