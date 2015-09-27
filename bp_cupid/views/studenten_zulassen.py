from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from bp_cupid.models import (
    Student,
)

import logging
logger = logging.getLogger(__name__)


@login_required
@user_passes_test(lambda u: u.is_staff)
def studenten_zulassen(request):
    akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum

    studenten = Student.objects.filter(
        verwaltungszeitraum=akt_verw_zr
    ).order_by('mat_nr')

    context = {
        'akt_verw_zeitraum': akt_verw_zr,
        'studenten': studenten,
    }

    if request.method == 'POST':
        mat_nrs = request.POST.get('matrikelnummern', '').split()
        try:
            mat_nrs = list(map(int, mat_nrs))
        except ValueError:
            messages.add_message(
                request,
                messages.ERROR,
                'Irgendeine von den Matrikelnummern war keine Zahl.',
            )
            return render(request, 'bp_cupid/studenten_zulassen.html', context)

        erzeugte_studenten = []
        for mat_nr in mat_nrs:
            student, created = Student.objects.get_or_create(
                mat_nr=mat_nr,
                defaults={
                    'verwaltungszeitraum': akt_verw_zr,
                }
            )
            if created:
                erzeugte_studenten.append(mat_nr)
                logger.debug('Student erzeugt: {}'.format(student.mat_nr))

        if erzeugte_studenten:
            messages.add_message(
                request,
                messages.SUCCESS,
                'Folgende Studenten wurden angelegt: {}'.format(
                    ', '.join(map(str, erzeugte_studenten))
                ),
            )

    studenten = Student.objects.filter(
        verwaltungszeitraum=akt_verw_zr
    ).order_by('mat_nr')

    context['studenten'] = studenten

    return render(request, 'bp_cupid/studenten_zulassen.html', context)
