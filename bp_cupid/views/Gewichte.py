from django.shortcuts import render
from django.core.cache import cache
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import View

from actstream import action

from ..tasks import berechne_gewichte, BERECHNE_GEWICHTE_LOCK_ID


class Gewichte(View):
    template_name = 'bp_cupid/gewichte.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request):
        """
        Zeigt die Berechnungsübersicht für die Gewichte an.
        """

        context = {
            'laufende_Gewichtsberechnung': self.gewichtsberechnung_laeuft(),
        }

        return render(request, self.template_name, context)


    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def post(self, request):
        """
        Startet die Gewichtsberechnung, falls nicht schon eine läuft.
        """
        if not self.gewichtsberechnung_laeuft():
            akt_verw_zr_id = request.user.mitarbeiter.akt_verw_zeitraum_id

            berechne_gewichte.delay(akt_verw_zr_id)
            action.send(
                request.user,
                verb='startete Gewichtsberechnung'
            )

        context = {
            'laufende_Gewichtsberechnung': self.gewichtsberechnung_laeuft(),
        }

        return render(request, self.template_name, context)


    def gewichtsberechnung_laeuft(self):
        return bool(cache.get(BERECHNE_GEWICHTE_LOCK_ID))
