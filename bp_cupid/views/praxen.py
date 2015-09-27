from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from bp_cupid.models import Praxis


@login_required
@user_passes_test(lambda u: u.is_staff)
def praxen(request):
    """
    Zeigt alle Praxen in einer Tabelle nach Nachname sortiert an.
    """
    praxen = Praxis.objects.order_by('name').select_related('landkreis')

    context = {
        'praxen': praxen,
    }

    return render(request, 'bp_cupid/praxen.html', context)
