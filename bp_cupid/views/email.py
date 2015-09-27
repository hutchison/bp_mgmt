from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, HttpResponse
from django.template import Template, Context
from django.utils.html import escape
from django.contrib import messages
from django.core.mail import (
    EmailMessage,
    get_connection,
)

from itertools import zip_longest

from ..models import (
    Vorlage,
    Platz,
    Student,
)

@login_required
@user_passes_test(lambda u: u.is_staff)
def email(request):
    akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum
    akt_bloecke = akt_verw_zr.bloecke.order_by('name')

    if akt_bloecke:
        platzlisten = [b.plaetze() for b in akt_bloecke]
        # Transponiere die Liste der Plätze, damit wir sie als Tabelle
        # darstellen können:
        blocklisten = zip_longest(*platzlisten)
    else:
        blocklisten = []

    vorlagen = Vorlage.objects.all()

    freie_studenten = Student.objects.frei().select_related(
        'verwaltungszeitraum'
    )

    context = {
        'bloecke': akt_bloecke,
        'blocklisten': blocklisten,
        'vorlagen': vorlagen,
        'freie_studenten': freie_studenten,
    }

    if request.method == 'POST':
        mat_nrs = map(int, request.POST.getlist('student'))

        studenten = Student.objects.filter(mat_nr__in=mat_nrs).order_by('name')
        plaetze = Platz.objects.filter(student__in=studenten)

        betreff = request.POST.get('email-subject', '').strip()
        email_vorlage = Template(request.POST.get('email-content', '').strip())
        bcc_addr = request.POST.get('email-bcc', '').strip()
        testmail = 'testmail' in request.POST

        emails = []
        recps = []

        sender = ''

        for student in studenten:
            recp = '{} {} <{}>'.format(
                student.vorname,
                student.name,
                student.email,
            )
            try:
                platz = plaetze.get(student=student)
            except Platz.DoesNotExist:
                platz = None

            email = EmailMessage(
                subject=betreff,
                body=email_vorlage.render(
                    Context({'student': student, 'platz': platz})
                ),
                from_email=sender,
            )

            """
            Falls wir eine Testmail verschicken wollen, dann wird die generierte
            E-Mail an die Adresse vom BCC-Feld geschickt:
            """
            if testmail:
                email.to = [bcc_addr]
            else:
                email.to = [recp]
                email.bcc = [bcc_addr]

            emails.append(email)
            recps.append(recp)

        with get_connection() as connection:
            for email in emails:
                email.connection = connection
                email.send()

        msg = """
        E-Mail wurde an folgende Studenten versandt:
        <ul>
        """
        for recp in recps:
            msg += '<li>{}</li>'.format(escape(recp))
        msg += '</ul>'

        messages.add_message(
            request,
            messages.SUCCESS,
            msg,
        )

    return render(request, 'bp_cupid/email.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def preview_email(request):
    """
    Erstellt eine Vorschau der übergebenen Vorlage.
    """
    if request.method == 'POST':
        akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum
        student = Student.objects.filter(
            verwaltungszeitraum=akt_verw_zr
        ).order_by('?').first()

        try:
            platz = student.platz
        except Platz.DoesNotExist:
            platz = None

        vorlagen_text = Template(request.POST.get('content', ''))
        context = Context({'student': student, 'platz': platz})

        preview = vorlagen_text.render(context)
        return HttpResponse(preview)
    else:
        raise Http404
