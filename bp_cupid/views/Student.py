from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import View

from ..models import (
    Student,
    Gewicht,
    Platz,
    Zeitraum,
)


class StudentDetail(View):
    template_name = 'bp_cupid/student.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request, mat_nr):
        """
        Zeigt die Gewichte zu allen Praxen vom ausgewählten Studenten an.
        """
        s = get_object_or_404(Student, mat_nr=mat_nr)

        akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum
        aktuelle_zeitraeume = Zeitraum.objects.filter(
            block__verwaltungszeitraum=akt_verw_zr,
        )

        gewichte = Gewicht.objects.filter(
            student__mat_nr=mat_nr
        ).prefetch_related('praxis__freie_zeitraeume').order_by('-wert')

        try:
            platz = Platz.objects.select_related('praxis').get(student=s)
        except Platz.DoesNotExist:
            platz = None

        context = {
            'student': s,
            'gewichte': gewichte,
            'platz': platz,
            'aktuelle_zeitraeume': aktuelle_zeitraeume,
        }

        return render(request, self.template_name, context)


class StudentList(View):
    template_name = 'bp_cupid/studenten.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request):
        """
        Zeigt alle Studenten in einer Tabelle nach Nachname sortiert an.
        """
        akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum

        context = {
            'studenten': Student.objects.filter(
                verwaltungszeitraum=akt_verw_zr
            ).select_related(
                'platz'
            ).prefetch_related(
                'landkreise',
                'bevorzugte_praxen',
            ).order_by('name'),
        }

        anz_studis = Student.objects.filter(
            verwaltungszeitraum=akt_verw_zr
        ).count()

        if anz_studis:
            anz_studis_mit_fragebogen = Student.objects.filter(
                verwaltungszeitraum=akt_verw_zr,
                hat_fragebogen_ausgefuellt=True,
            ).count()

            rel_fragebogen = round(
                100 * anz_studis_mit_fragebogen / anz_studis, 1
            )

            context.update(
                {
                    'anz_studis': anz_studis,
                    'anz_studis_mit_fragebogen': anz_studis_mit_fragebogen,
                    'rel_fragebogen': rel_fragebogen,
                }
            )

        return render(request, self.template_name, context)
