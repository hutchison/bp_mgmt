from django.shortcuts import render
from django.core.cache import cache
from django.contrib.auth.decorators import login_required, user_passes_test
from actstream import action
from bp_cupid.tasks import verteile_studenten_task, VERTEILE_PLAETZE_LOCK_ID
from bp_cupid.models import (
    Student,
)

import logging
logger = logging.getLogger(__name__)


@login_required
@user_passes_test(lambda u: u.is_staff)
def verteilen(request):
    """
    View für die zufällige Verteilung von Studenten an Praxen.
    """
    akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum
    bloecke = akt_verw_zr.bloecke.order_by('name').prefetch_related(
        'zeitraeume__plaetze',
    )

    context = {
        'bloecke': bloecke,
        'anzahl_freie_studenten': Student.objects.frei().filter(
                verwaltungszeitraum=akt_verw_zr,
            ).count(),
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

    return render(request, 'bp_cupid/verteilen.html', context)
