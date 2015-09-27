from django.shortcuts import redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from bp_cupid.models import (
    ZusatzinfoPraxis,
)


@login_required
@user_passes_test(lambda u: u.is_staff)
def zusatzinfo(request):
    if request.method == 'POST':
        praxis_id = int(request.POST.get('praxis_id'))
        verwaltungszeitraum_id = int(request.POST.get('verwaltungszeitraum_id'))
        text = request.POST.get('zusatzinfo_text').strip()

        ZusatzinfoPraxis.objects.update_or_create(
            praxis_id=praxis_id,
            verwaltungszeitraum_id=verwaltungszeitraum_id,
            defaults={'text': text},
        )

        return redirect('bp_cupid:praxis', praxis_id=praxis_id)
    else:
        raise Http404
