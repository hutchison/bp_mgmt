from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from bp_cupid.models import (
    Praxis,
    Gewicht,
    ZusatzinfoPraxis,
)


@login_required
@user_passes_test(lambda u: u.is_staff)
def praxis(request, praxis_id):
    """
    Zeigt die Gewichte der gewählten Praxis von allen Studenten des aktuellen
    Verwaltungszeitraums an.
    """
    p = get_object_or_404(
        Praxis.objects.prefetch_related(
            'zeitraeume',
            'plaetze',
            'freie_zeitraeume',
        ),
        id=praxis_id
    )
    akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum

    anzahl_plaetze = p.plaetze.filter(
        zeitraum__block__verwaltungszeitraum=akt_verw_zr
    ).count()
    zeitraeume = p.zeitraeume.filter(block__verwaltungszeitraum=akt_verw_zr)
    gewichte = Gewicht.objects.filter(
        praxis__id=praxis_id,
        student__verwaltungszeitraum=akt_verw_zr,
    ).order_by('-wert').prefetch_related('student__platz__zeitraum')

    try:
        zusatzinfo = ZusatzinfoPraxis.objects.get(
            praxis_id=praxis_id,
            verwaltungszeitraum=akt_verw_zr,
        )
    except ZusatzinfoPraxis.DoesNotExist:
        zusatzinfo = None

    context = {
        'praxis': p,
        'anzahl_plaetze': anzahl_plaetze,
        'zeitraeume': zeitraeume,
        'gewichte': gewichte,
        'verwaltungszeitraum': akt_verw_zr,
        'zusatzinfo': zusatzinfo,
    }

    try:
        pgrenze = p.platzbegrenzung.get(verwaltungszeitraum=akt_verw_zr)
        context['platzbegrenzung'] = pgrenze.anzahl
    except:
        pass

    return render(request, 'bp_cupid/praxis.html', context)
