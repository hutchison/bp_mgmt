from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from ..models import (
    Verwaltungszeitraum,
    Mitarbeiter,
)

@login_required
@user_passes_test(lambda u: u.is_staff)
def einstellungen(request):
    mitarbeiter = Mitarbeiter.objects.get(user=request.user)
    akt_verw_zr = mitarbeiter.akt_verw_zeitraum
    verwzrs = Verwaltungszeitraum.objects.order_by('-anfang')

    context = {
        'akt_verw_zeitraum': akt_verw_zr,
        'verwzrs': verwzrs,
    }

    if request.method == 'POST':
        neue_verw_zr_id = int(request.POST.get('verwaltungszeitraum'))
        neuer_verw_zr = Verwaltungszeitraum.objects.get(id=neue_verw_zr_id)
        mitarbeiter.akt_verw_zeitraum = neuer_verw_zr
        mitarbeiter.save()
        context['akt_verw_zeitraum'] = neuer_verw_zr

    return render(request, 'bp_cupid/einstellungen.html', context)
