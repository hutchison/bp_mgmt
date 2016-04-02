from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import View

from actstream import action

from ..models import Platz, Evaluation
from ..forms import EvaluationForm

class EvaluationList(View):
    template_name = 'bp_cupid/evaluationenliste.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request):
        """
        Zeigt alle Plätze mit den Evaluationen an.
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
            'evaluation',
        )

        context = {
            'plaetze': plaetze,
        }

        return render(request, self.template_name, context)


class EvaluationDetail(View):
    form_class = EvaluationForm
    template_name = 'bp_cupid/evaluation.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request, mat_nr):
        """
        Zeigt das Evaluationsformular an.
        """

        platz = get_object_or_404(Platz, student__mat_nr=mat_nr)
        user = request.user

        initial_data = {
            'platz': platz,
            'eval_user': user,
        }

        """
        Falls schon eine Evaluation existiert, dann laden wir die Daten davon.
        """
        try:
            ev = platz.evaluation
        except Evaluation.DoesNotExist:
            ev = None

        form = self.form_class(initial=initial_data, instance=ev)

        context = {
            'form': form,
            'akt_datum': now(),
            'platz': platz,
        }

        return render(request, self.template_name, context)

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def post(self, request, mat_nr):
        """
        Speichert eine Evaluation. Wenn schon eine Evaluation existiert, wird
        die alte überschrieben.
        """
        try:
            ev = Evaluation.objects.get(platz__student__mat_nr=mat_nr)
        except Evaluation.DoesNotExist:
            ev = None

        form = self.form_class(request.POST, instance=ev)

        if form.is_valid():
            neue_evaluation = form.save()

            if ev:
                action_verb = 'bearbeitete die Evaluation von'
            else:
                action_verb = 'evaluierte'

            action.send(
                request.user,
                verb=action_verb,
                target=neue_evaluation.platz.student,
            )

            return redirect('bp_cupid:evaluation_uebersicht')
        else:
            """
            Falls beim Formular ein Fehler aufgetreten ist, dann suchen wir uns
            wieder den Platz raus und stellen das Formular mit den bereits
            eingegebenen Daten dar:
            """
            platz = get_object_or_404(Platz, student__mat_nr=mat_nr)
            context = {
                'form': form,
                'akt_datum': now(),
                'platz': platz,
            }
            return render(request, self.template_name, context)
