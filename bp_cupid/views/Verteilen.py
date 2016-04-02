from django.shortcuts import render
from django.core.cache import cache
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import View

from actstream import action
from random import choice
import logging
logger = logging.getLogger(__name__)

from ..models import (
    Block,
    Platz,
    Student,
)
from ..tasks import verteile_studenten_task, VERTEILE_PLAETZE_LOCK_ID


class ZufaelligVerteilen(View):
    template_name = 'bp_cupid/zufaellig_verteilen.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request):
        """
        Zeigt die zufällige Verteilung von Studenten an Praxen an.
        """
        context = self.common_context(request.user.mitarbeiter.akt_verw_zeitraum)

        if cache.get(VERTEILE_PLAETZE_LOCK_ID):
            context['laufende_Platzverteilung'] = True

        return render(request, self.template_name, context)


    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def post(self, request):
        """
        Startet die zufällige Platzverteilung.
        """
        context = self.common_context(request.user.mitarbeiter.akt_verw_zeitraum)

        if not cache.get(VERTEILE_PLAETZE_LOCK_ID):
            gewaehlte_bloecke = [int(b) for b in request.POST.getlist('block')]
            anzahl_studenten = request.POST.get('anzahl_studenten')
            blocklimit = request.POST.get('blocklimit')

            loeschen = bool(request.POST.get('loeschen', False))

            action.send(
                request.user,
                verb='startete zufällige Platzverteilung'
            )

            verteile_studenten_task.delay(
                anzahl_studenten,
                blocklimit,
                gewaehlte_bloecke,
                loeschen,
            )

            context['laufende_Platzverteilung'] = True

        return render(request, self.template_name, context)


    @staticmethod
    def common_context(akt_verw_zr):
        """
        Gibt gemeinsamen Kontext für GET und POST zurück.
        """
        bloecke = akt_verw_zr.bloecke.order_by('name').prefetch_related(
            'zeitraeume__plaetze',
        )
        freie_studenten = Student.objects.frei().filter(
            hat_fragebogen_ausgefuellt=True,
            verwaltungszeitraum=akt_verw_zr,
        )

        context = {
            'bloecke': bloecke,
            'anzahl_freie_studenten': freie_studenten.count(),
        }

        return context


class GezieltVerteilen(View):
    template_name = 'bp_cupid/gezielt_verteilen.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request):
        """
        Zeigt die gezielte Verteilung von Studenten auf Blöcke an.
        """
        context = self.common_context(request.user.mitarbeiter.akt_verw_zeitraum)

        return render(request, self.template_name, context)


    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def post(self, request):
        """
        Startet die gezielte Verteilung.
        """
        block_id = int(request.POST.get('block'))
        block = Block.objects.get(id=block_id)

        mat_nrs = map(int, request.POST.getlist('student'))
        studenten = Student.objects.filter(mat_nr__in=mat_nrs)

        action.send(
            request.user,
            verb='startete gezielte Platzverteilung'
        )
        plaetze = self.verteile_studenten_auf_block(studenten, block)

        context = self.common_context(request.user.mitarbeiter.akt_verw_zeitraum)
        context['plaetze'] = plaetze

        return render(request, self.template_name, context)


    def common_context(self, akt_verw_zr):
        """
        Gibt gemeinsamen Kontext für GET und POST zurück.
        """
        bloecke = akt_verw_zr.bloecke.order_by('name').prefetch_related(
            'zeitraeume__plaetze',
        )

        context = {
            'freie_studenten': Student.objects.frei().order_by('name'),
            'bloecke': bloecke,
        }

        return context


    @staticmethod
    def verteile_studenten_auf_block(studenten, block):
        studenten = list(studenten)
        logger.debug(
            "Verteile die Studenten {} auf Block {}".format(
                studenten,
                block
            )
        )
        plaetze = []

        """
        TODO: das muss ich mal überarbeiten.
        Wir prüfen hier, ob ein Student Gewichte hat. Eigentlich sollten wir
        sicherstellen, dass immer alle Gewichte vorhanden sind, oder aber die
        Gewichte berechnen, wenn wir sie brauchen.
        """
        while studenten:
            student = choice(studenten)
            logger.debug("Versuche Student {} zu verteilen".format(student))
            logger.debug("dieser hat {} Gewichte".format(student.gewichte.count()))

            if student.gewichte.exists():
                for gewicht in student.gewichte.order_by('-wert'):
                    praxis = gewicht.praxis
                    if praxis.hat_platz_in_block(block):
                        zeitraum = praxis.freie_zeitraeume_in_block(block)[0]
                        platz = Platz.vergib_platz(
                            student.id,
                            praxis.id,
                            zeitraum.id
                        )
                        student.verwaltungszeitraum = block.verwaltungszeitraum
                        student.save()
                        plaetze.append(platz)
                        studenten.remove(student)
                        break
            else:
                logger.debug(
                    'Überspringe Student {}, weil keine Gewichte '
                    'vorhanden sind.'.format(student)
                )
                studenten.remove(student)

        return plaetze
