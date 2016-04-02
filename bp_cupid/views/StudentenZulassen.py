from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View

from ..models import (
    Student,
)

import logging
logger = logging.getLogger(__name__)


class StudentenZulassen(View):
    template_name = 'bp_cupid/studenten_zulassen.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request):
        """
        Zeigt alle Studenten vom eingestellten Verwaltungszeitraum an und dazu
        ein Textfeld, in das man Matrikelnummern eingeben kann, zu welchen dann
        Studenten erzeugt werden.
        """
        akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum

        studenten = Student.objects.filter(
            verwaltungszeitraum=akt_verw_zr
        ).order_by('mat_nr')

        context = {
            'akt_verw_zeitraum': akt_verw_zr,
            'studenten': studenten,
        }

        return render(request, self.template_name, context)

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def post(self, request):
        """
        Legt die Studenten an, deren Matrikelnummern übergeben wurden.
        """
        akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum
        mat_nrs = request.POST.get('matrikelnummern', '').split()

        studenten = Student.objects.filter(
            verwaltungszeitraum=akt_verw_zr
        ).order_by('mat_nr')

        context = {
            'studenten': studenten,
        }

        try:
            mat_nrs = list(map(int, mat_nrs))
        except ValueError:
            messages.add_message(
                request,
                messages.ERROR,
                'Irgendeine von den Matrikelnummern war keine Zahl.',
            )
            return render(request, self.template_name, context)

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

        return render(request, self.template_name, context)
