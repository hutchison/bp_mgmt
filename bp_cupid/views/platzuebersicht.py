from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from bp_cupid.models import (
    Praxis,
    Zeitraum,
    Platzbegrenzung,
)
from collections import OrderedDict


@login_required
@user_passes_test(lambda u: u.is_staff)
def platzuebersicht(request):
    akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum
    bloecke = akt_verw_zr.bloecke.order_by('name').prefetch_related(
        'zeitraeume'
    )
    zeitraeume = Zeitraum.objects.filter(
        block__in=bloecke
    ).order_by(
        'anfang'
    )

    context = {
        'akt_verw_zr': akt_verw_zr,
        'bloecke': bloecke,
        'zeitraeume': zeitraeume,
        'kapazitaeten': kapazitaeten(akt_verw_zr),
        'platztabelle': platztabelle(zeitraeume),
    }

    return render(request, 'bp_cupid/platzuebersicht.html', context)

def kapazitaeten(verwaltungszeitraum):
    kap = []
    praxen = Praxis.objects.prefetch_related('zeitraeume')

    bloecke = verwaltungszeitraum.bloecke.order_by('name')
    bloecke = bloecke.prefetch_related('zeitraeume__plaetze')
    bloecke = bloecke.annotate(Count('zeitraeume'))
    """
    TODO: Leider gibt’s beim folgenden Query falsche Ergebnisse bei der
    maximalen Kapazität. Falls wir das beheben könnten, würde die Anzahl der
    Queries auf 16 absinken und alles wäre mit Regenbögen und Einhörnern
    geschmückt. Leider weiß ich nicht wie. Ein einfaches distinct() reicht
    nicht.
    """
    # bloecke = bloecke.prefetch_related('zeitraeume__ueberlappende')

    for block in bloecke:
        k = {}
        k['name'] = block.name
        k['anz_zr'] = block.zeitraeume__count
        k['vergebene_plaetze'] = block.anzahl_plaetze()
        k['max_kap'] = sum([p.kapazitaet(block) for p in praxen])
        kap.append(k)

    return kap

def platztabelle(zeitraeume):
    """
    Gibt die Platztabelle der übergebenen Zeiträume zurück.

    Die Platztabelle ist ein OrderedDict. Die Schlüssel sind die Praxen. Zu
    jeder Praxis gibt es eine Liste. Die Elemente dieser Liste sind entweder:
        * Plätze
            dann ist dieser Zeitraum mit einem Platz belegt
        * Zeiträume
            dann ist der Zeitraum noch frei
        * None
            dann ist der Zeitraum durch einen anderen Platz belegt
    """
    akt_verw_zr = zeitraeume.first().block.verwaltungszeitraum
    praxen = Praxis.objects.filter(
        ist_aktiv=True
    ).order_by(
        'name'
    ).prefetch_related(
        'freie_zeitraeume',
        'plaetze__zeitraum',
        'plaetze__student',
    )
    platztabelle = OrderedDict()

    for praxis in praxen:
        platztabelle[praxis] = list(
            praxis.plaetze.filter(zeitraum__in=zeitraeume)
        )
        direkt_belegte_zrs = [
            platz.zeitraum
            for platz in praxis.plaetze.filter(zeitraum__in=zeitraeume)
        ]
        for i, zeitraum in enumerate(zeitraeume):
            if zeitraum in direkt_belegte_zrs:
                continue
            elif zeitraum in praxis.freie_zeitraeume.all():
                platztabelle[praxis].insert(i, zeitraum)
            else:
                platztabelle[praxis].insert(i, None)

        akt_anzahl_plaetze = praxis.plaetze.filter(
            zeitraum__block__verwaltungszeitraum=akt_verw_zr,
        ).count()
        try:
            platzgrenze = praxis.platzbegrenzung.get(
                verwaltungszeitraum=akt_verw_zr
            ).anzahl
        except Platzbegrenzung.DoesNotExist:
            platzgrenze = None
        platztabelle[praxis].append(
            (akt_anzahl_plaetze, platzgrenze)
        )

    return platztabelle
