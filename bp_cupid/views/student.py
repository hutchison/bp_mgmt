from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from bp_cupid.models import (
    Student,
    Gewicht,
    Platz,
    Zeitraum,
)


@login_required
@user_passes_test(lambda u: u.is_staff)
def student(request, mat_nr):
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

    return render(request, 'bp_cupid/student.html', context)
