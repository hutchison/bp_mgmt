from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import View

from ..models import Praxis


class Praxen(View):
    template_name = 'bp_cupid/praxen.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request):
        """
        Zeigt alle Praxen in einer Tabelle nach Nachname sortiert an.
        """
        praxen = Praxis.objects.order_by('name').select_related('landkreis')

        context = {
            'praxen': praxen,
        }

        return render(request, self.template_name, context)
