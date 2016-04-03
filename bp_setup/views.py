from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View

from actstream import action
import logging
logger = logging.getLogger(__name__)

from bp_cupid.models import (
    Landkreis,
    Praxis,
    Student,
)


class Index(View):
    template_name = 'bp_setup/index.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: Student.objects.filter(user=u).exists()))
    def get(self, request):
        student = Student.objects.get(user=request.user)

        context = {
            'student': student,
        }

        return render(request, self.template_name, context)


class Fragebogen(View):
    template_name = 'bp_setup/fragebogen.html'

    @method_decorator(login_required)
    def get(self, request):
        """
        Zeigt den Fragebogen für Studenten an.
        """
        context = self.common_context(request)
        student = context['student']

        if student and student.hat_fragebogen_ausgefuellt:
            messages.add_message(
                request,
                messages.INFO,
                'Clever! Aber leider hast du den Fragebogen schon ausgefüllt.',
            )
            return redirect('bp_setup:index')
        else:
            return render(request, self.template_name, context)


    @method_decorator(login_required)
    def post(self, request):
        """
        Speichert die Daten des Fragebogens ab.
        """

        context = self.common_context(request)
        student = context['student']

        # erst aufräumen:
        for praxis in student.bevorzugte_praxen.all():
            student.bevorzugte_praxen.remove(praxis)

        for praxis in student.abgeneigte_praxen.all():
            student.abgeneigte_praxen.remove(praxis)

        for landkreis in student.landkreise.all():
            student.landkreise.remove(landkreis)

        # dann die Daten des Fragebogens speichern:
        besondere_kriterien = request.POST.get('besondere_praxiskriterien', '')
        student.besondere_praxiskriterien = besondere_kriterien

        gew_kinder = int(request.POST.get('kinder', 0))
        student.gewichtung_kinder = gew_kinder

        gew_sono = int(request.POST.get('sono', 0))
        student.gewichtung_sono = gew_sono

        gew_sport = int(request.POST.get('sport', 0))
        student.gewichtung_sport = gew_sport

        gew_kompl = int(request.POST.get('kompl', 0))
        student.gewichtung_kompl = gew_kompl

        gew_hohe_duene = int(request.POST.get('hoheduene', 0))
        student.gewichtung_hohe_duene = gew_hohe_duene

        fs_und_fahrzeug = bool(int(request.POST.get('fsundauto', 0)))
        student.fs_und_fahrzeug = fs_und_fahrzeug

        gewaehlte_praxen_ids = map(int, request.POST.getlist('praxis'))
        if gewaehlte_praxen_ids:
            gewaehlte_praxen = Praxis.objects.filter(id__in=gewaehlte_praxen_ids)
            for praxis in gewaehlte_praxen:
                student.bevorzugte_praxen.add(praxis)

        gewaehlte_landkreise_ids = map(int, request.POST.getlist('landkreis'))
        gewaehlte_landkreise = Landkreis.objects.filter(id__in=gewaehlte_landkreise_ids)
        for landkreis in gewaehlte_landkreise:
            student.landkreise.add(landkreis)

        uebernachtung = bool(int(request.POST.get('uebernachtung', 0)))
        adresse_priv_unterkunft = request.POST.get('uebernachtungsort', '')

        student.priv_unterkunft = uebernachtung
        student.adresse_priv_unterkunft = adresse_priv_unterkunft

        sonstiges = request.POST.get('ergaenzungen', '')
        student.sonstiges = sonstiges

        student.hat_fragebogen_ausgefuellt = True

        student.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            'Vielen Dank für’s Ausfüllen!',
        )

        action.send(
            request.user,
            verb='füllte den Fragebogen aus'
        )

        return redirect('bp_setup:index')


    @staticmethod
    def common_context(request):
        besondere_la_praxen_ids = [10, 46, 59]
        besondere_la_praxen = Praxis.objects.filter(
            id__in=besondere_la_praxen_ids,
        )

        landkreise = Landkreis.objects.order_by('plz_von')

        try:
            student = request.user.student
        except Student.DoesNotExist:
            student = None

        context = {
            'besondere_la_praxen': besondere_la_praxen,
            'student': student,
            'landkreise': landkreise,
        }

        return context
