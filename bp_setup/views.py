from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from bp_cupid.models import (
    Praxis,
    Student,
    Landkreis,
)
from actstream import action

import logging
logger = logging.getLogger(__name__)


@login_required
@user_passes_test(lambda u: Student.objects.filter(user=u).exists())
def index(request):
    student = Student.objects.get(user=request.user)

    context = {
        'student': student,
    }

    return render(request, 'bp_setup/index.html', context)


@login_required
def fragebogen(request):
    besondere_la_praxen_ids = []
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


    if student and student.hat_fragebogen_ausgefuellt:
        messages.add_message(
            request,
            messages.INFO,
            'Clever! Aber leider hast du den Fragebogen schon ausgefüllt.',
        )
        return redirect('bp_setup:index')

    if request.method == 'POST':
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

    return render(request, 'bp_setup/fragebogen.html', context)
