from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.http import urlquote
from django.views.generic import View

from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.flowables import PageBreak

from ..models import Praxis


class PDFPraxis(View):

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request, praxis_id):
        """
        Gibt eine PDF-Datei mit einer Übersicht der verteilten Plätze für die
        Praxis zurück.
        """
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


class PDFPraxen(View):

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request):
        """
        Gibt eine PDF-Datei mit einer Übersicht der verteilten Plätze für alle
        Praxen zurück.
        """
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
