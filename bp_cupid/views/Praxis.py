from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import View

from ..models import (
    Praxis,
    Gewicht,
    ZusatzinfoPraxis,
)


class PraxisDetail(View):
    template_name = 'bp_cupid/praxis.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request, praxis_id):
        """
        Zeigt die Gewichte der gewählten Praxis von allen Studenten des
        aktuellen Verwaltungszeitraums an.
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
        zeitraeume = p.zeitraeume.filter(
            block__verwaltungszeitraum=akt_verw_zr
        )
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

        return render(request, self.template_name, context)


class PraxisList(View):
    template_name = 'bp_cupid/praxen.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request):
        """
        Zeigt alle Praxen in einer Tabelle nach Nachname sortiert an.
        """
        praxen = Praxis.objects.order_by('name').select_related('landkreis')

        context = {
            'praxen': praxen,
        }

        return render(request, self.template_name, context)
