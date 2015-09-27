from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from itertools import zip_longest

@login_required
@user_passes_test(lambda u: u.is_staff)
def bloecke(request):
    akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum
    akt_bloecke = akt_verw_zr.bloecke.order_by('name')

    if akt_bloecke:
        platzlisten = [b.plaetze() for b in akt_bloecke]
        # Transponiere die Liste der Plätze, damit wir sie als Tabelle
        # darstellen können:
        blocklisten = zip_longest(*platzlisten)
    else:
        blocklisten = []

    context = {
        'bloecke': akt_bloecke,
        'blocklisten': blocklisten,
    }

    return render(request, 'bp_cupid/bloecke.html', context)
