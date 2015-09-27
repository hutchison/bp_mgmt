from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.utils.http import urlquote

from reportlab.platypus.flowables import PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate
from io import BytesIO

from bp_cupid.models import (
    Praxis,
)


@login_required
@user_passes_test(lambda u: u.is_staff)
def praxis(request, praxis_id):
    praxis = get_object_or_404(Praxis, id=praxis_id)
    akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum
    pdf = praxis.pdf(verwaltungszeitraum=akt_verw_zr)

    dateiname = 'Praxis {} {}.pdf'.format(praxis.vorname, praxis.name)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = """attachment;\
        filename="{0}";\
        filename*=UTF-8''{0};\
    """.format(urlquote(dateiname))
    response.write(pdf)

    return response


@login_required
@user_passes_test(lambda u: u.is_staff)
def praxen(request):
    akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum
    elements = []

    for praxis in Praxis.objects.order_by('name'):
        hat_plaetze = praxis.plaetze.filter(
            zeitraum__block__verwaltungszeitraum=akt_verw_zr
        ).exists()
        if not hat_plaetze:
            continue

        elements.extend(
            praxis.pdf_elemente(verwaltungszeitraum=akt_verw_zr)
        )
        elements.append(PageBreak())

    with BytesIO() as buf:
        doc = SimpleDocTemplate(buf, pagesize=A4)
        doc.build(elements)
        pdf = buf.getvalue()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Praxen.pdf"'
    response.write(pdf)

    return response
