from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import View

from ..models import (
    Platz,
    Student,
)


class Plaetze(View):
    template_name = 'bp_cupid/plaetze.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request):
        """
        Gibt alle Plätze als Tabelle aus.
        """
        akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum

        plaetze = Platz.objects.filter(
            student__verwaltungszeitraum=akt_verw_zr,
        ).order_by(
            'student__name',
        ).select_related(
            'student',
            'praxis',
            'zeitraum',
        )

        context = {
            'plaetze': plaetze,
        }

        anzahl_plaetze = Platz.objects.filter(
            student__verwaltungszeitraum=akt_verw_zr,
        ).count()

        if anzahl_plaetze:
            automatische_plaetze = Platz.objects.filter(
                student__verwaltungszeitraum=akt_verw_zr,
                manuell=False,
            ).count()
            rel_automatische = round(
                100 * automatische_plaetze / anzahl_plaetze, 3
            )
            manuelle_plaetze = Platz.objects.filter(
                student__verwaltungszeitraum=akt_verw_zr,
                manuell=True,
            ).count()
            rel_manuelle = round(
                100 * manuelle_plaetze / anzahl_plaetze, 3
            )
            externe = Student.objects.filter(
                verwaltungszeitraum=akt_verw_zr,
                extern=True,
            ).count()
            rel_externe = round(
                100 * externe / anzahl_plaetze, 3
            )

            context.update(
                {
                    'anzahl_plaetze': anzahl_plaetze,
                    'automatische_plaetze': automatische_plaetze,
                    'rel_automatische': rel_automatische,
                    'manuelle_plaetze': manuelle_plaetze,
                    'rel_manuelle': rel_manuelle,
                    'externe': externe,
                    'rel_externe': rel_externe,
                }
            )
        return render(request, self.template_name, context)
