from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View

from ..models import Verwaltungszeitraum


class Einstellungen(View):
    template_name = 'bp_cupid/einstellungen.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request):
        """
        Zeigt das Formular für die Einstellungen an.
        """
        context = self.common_context(request.user.mitarbeiter)

        return render(request, self.template_name, context)


    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def post(self, request):
        """
        Speichert die Einstellungen für einen Mitarbeiter.
        """
        mitarbeiter = request.user.mitarbeiter
        context = self.common_context(request.user.mitarbeiter)

        neue_verw_zr_id = int(request.POST.get('verwaltungszeitraum'))
        neuer_verw_zr = Verwaltungszeitraum.objects.get(id=neue_verw_zr_id)

        mitarbeiter.akt_verw_zeitraum = neuer_verw_zr
        mitarbeiter.save()

        context['akt_verw_zeitraum'] = neuer_verw_zr
        context['gespeichert'] = True

        return render(request, self.template_name, context)


    @staticmethod
    def common_context(mitarbeiter):
        akt_verw_zr = mitarbeiter.akt_verw_zeitraum
        verwzrs = Verwaltungszeitraum.objects.order_by('-anfang')

        context = {
            'akt_verw_zeitraum': akt_verw_zr,
            'verwzrs': verwzrs,
        }

        return context
