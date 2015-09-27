from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from bp_cupid.models import Student


@login_required
@user_passes_test(lambda u: u.is_staff)
def studenten(request):
    """
    Zeigt alle Studenten in einer Tabelle nach Nachname sortiert an.
    """
    akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum

    context = {
        'studenten': Student.objects.filter(
            verwaltungszeitraum=akt_verw_zr
        ).select_related('platz').prefetch_related(
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
        rel_fragebogen = round(100 * anz_studis_mit_fragebogen / anz_studis, 1)

        context.update(
            {
                'anz_studis': anz_studis,
                'anz_studis_mit_fragebogen': anz_studis_mit_fragebogen,
                'rel_fragebogen': rel_fragebogen,
            }
        )

    return render(request, 'bp_cupid/studenten.html', context)
