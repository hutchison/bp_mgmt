from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import View

from ..models import ZusatzinfoPraxis


class Zusatzinfo(View):

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def post(self, request):
        """
        Erstellt oder aktualisiert die Zusatzinformationen zu einer Praxis.
        """
        praxis_id = int(request.POST.get('praxis_id'))
        verwaltungszeitraum_id = int(request.POST.get('verwaltungszeitraum_id'))
        text = request.POST.get('zusatzinfo_text').strip()

        ZusatzinfoPraxis.objects.update_or_create(
            praxis_id=praxis_id,
            verwaltungszeitraum_id=verwaltungszeitraum_id,
            defaults={'text': text},
        )

        return redirect('bp_cupid:praxis', praxis_id=praxis_id)
