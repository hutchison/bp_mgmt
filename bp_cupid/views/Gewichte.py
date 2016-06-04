from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import View

from actstream import action

from ..models import(
    Gewicht,
    Praxis,
    Student,
)
from ..tasks import berechne_gewichte, BERECHNE_GEWICHTE_LOCK_ID


class Gewichte(View):
    template_name = 'bp_cupid/gewichte.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request):
        """
        Zeigt die Berechnungsübersicht für die Gewichte an.
        """
        akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum

        akt_anzahl_studenten = Student.objects.filter(
            verwaltungszeitraum=akt_verw_zr
        ).count()
        anzahl_praxen = Praxis.objects.count()
        akt_anzahl_gewichte = Gewicht.objects.filter(
            student__verwaltungszeitraum=akt_verw_zr
        ).count()

        context = {
            'laufende_Gewichtsberechnung': self.gewichtsberechnung_laeuft(),
            'akt_anzahl_studenten': akt_anzahl_studenten,
            'anzahl_praxen': anzahl_praxen,
            'anzahl_gewichte_soll': akt_anzahl_studenten * anzahl_praxen,
            'anzahl_gewichte_haben': akt_anzahl_gewichte,
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

        return redirect('bp_cupid:gewichte')


    def gewichtsberechnung_laeuft(self):
        return bool(cache.get(BERECHNE_GEWICHTE_LOCK_ID))
