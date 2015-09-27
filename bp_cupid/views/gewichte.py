from django.shortcuts import render
from django.core.cache import cache
from django.contrib.auth.decorators import login_required, user_passes_test
from actstream import action
from bp_cupid.tasks import berechne_gewichte, BERECHNE_GEWICHTE_LOCK_ID


@login_required
@user_passes_test(lambda u: u.is_staff)
def gewichte(request):
    context = dict()

    if request.method == 'POST':
        if not cache.get(BERECHNE_GEWICHTE_LOCK_ID):
            akt_verw_zr_id = request.user.mitarbeiter.akt_verw_zeitraum_id

            berechne_gewichte.delay(akt_verw_zr_id)
            action.send(
                request.user,
                verb='startete Gewichtsberechnung'
            )
            context['laufende_Gewichtsberechnung'] = True

    if cache.get(BERECHNE_GEWICHTE_LOCK_ID):
        context['laufende_Gewichtsberechnung'] = True

    return render(request, 'bp_cupid/gewichte.html', context)
