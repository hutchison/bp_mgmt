from django.shortcuts import render
from django.views.generic import View

from collections import OrderedDict

from ..models import (
    Verwaltungszeitraum,
    Praxis,
    Student,
    Platz,
    Gewicht,
)


class Status(View):
    template_name = 'bp_cupid/status.html'

    def get(self, request):
        if request.user.is_authenticated() and request.user.is_staff:
            akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum
        else:
            akt_verw_zr = Verwaltungszeitraum.aktuell()

        fakten = OrderedDict()
        fakten['Anzahl Studenten'] = Student.objects.filter(
            verwaltungszeitraum=akt_verw_zr,
        ).count()
        fakten['Anzahl Praxen'] = Praxis.objects.count()
        fakten['davon mit BP-Plätzen'] = len(
            [p for p in Praxis.objects.prefetch_related('zeitraeume') if p.anzahl_zeitraeume()]
        )

        fakten['vergebene Plätze'] = Platz.objects.filter(
            zeitraum__block__verwaltungszeitraum=akt_verw_zr,
        ).count()

        context = {
            'fakten': fakten,
            'verwzr': akt_verw_zr,
        }

        return render(request, self.template_name, context)


def abweichung_automatischer_plaetze():
    """
    Berechnet die Abweichung der automatisch vergebenen Plätze vom theoretischen
    Optimum (wenn jeder Student das beste Gewicht abbekommen hätte).

    Angenommen Alice hätte von ihren Gewichten das 4. als Platz abbekommen. Dann
    wäre ihre Abweichung 4 - 1 = 3.
    """
    abweichung = 0
    for platz in Platz.objects.filter(manuell=False):
        platzgewicht = Gewicht.objects.get(
            student=platz.student,
            praxis=platz.praxis,
        )
        stud_gewichte = list(
            Gewicht.objects.filter(student=platz.student).order_by('-wert')
        )
        abweichung += stud_gewichte.index(platzgewicht)

    return abweichung
