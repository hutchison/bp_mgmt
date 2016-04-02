from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import (
    EmailMessage,
    get_connection,
)
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, Context
from django.template.base import TemplateSyntaxError
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.generic import View

from itertools import zip_longest

from ..models import (
    Vorlage,
    Platz,
    Student,
)


class Email(View):
    template_name = 'bp_cupid/email.html'
    vorlagen = Vorlage.objects.all()
    freie_studenten = Student.objects.frei().select_related(
        'verwaltungszeitraum'
    )


    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request):
        """
        Zeigt das Formular für den E-Mail-Versand an.
        """
        akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum
        akt_bloecke = akt_verw_zr.bloecke.order_by('name')

        context = {
            'bloecke': akt_bloecke,
            'blocklisten': self.blocklisten(akt_bloecke),
            'vorlagen': self.vorlagen,
            'freie_studenten': self.freie_studenten,
        }

        return render(request, self.template_name, context)


    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def post(self, request):
        """
        Bastelt die E-Mails zusammen und verschickt sie an die gewählten
        Studenten.
        """
        mat_nrs = map(int, request.POST.getlist('student'))

        studenten = Student.objects.filter(mat_nr__in=mat_nrs).order_by('name')
        plaetze = Platz.objects.filter(student__in=studenten)

        betreff = request.POST.get('email-subject', '').strip()
        email_vorlage = Template(request.POST.get('email-content', '').strip())
        bcc_addr = request.POST.get('email-bcc', '').strip()
        testmail = 'testmail' in request.POST

        emails = []
        recps = []

        sender = 'Team Lehre der Allgemeinmedizin <team.lehre@med.uni-rostock.de>'

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

        """
        Zuletzt basteln wir noch den Hinweis über die versandten E-Mails
        zurecht:
        """
        if testmail:
            msg = """
            Diese Testmail wäre an folgende Studenten versandt worden:
            <ul>
            """
            msg_type = messages.INFO
        else:
            msg = """
            E-Mail wurde an folgende Studenten versandt:
            <ul>
            """
            msg_type = messages.SUCCESS

        for recp in recps:
            msg += '<li>{}</li>'.format(escape(recp))
        msg += '</ul>'

        messages.add_message(request, msg_type, msg)

        akt_bloecke = self.aktuelle_bloecke(
            request.user.mitarbeiter.akt_verw_zeitraum
        )
        context = {
            'bloecke': akt_bloecke,
            'blocklisten': self.blocklisten(akt_bloecke),
            'vorlagen': self.vorlagen,
            'freie_studenten': self.freie_studenten,
        }

        return render(request, self.template_name, context)


    @staticmethod
    def blocklisten(bloecke):
        if bloecke:
            platzlisten = [b.plaetze() for b in bloecke]
            # Transponiere die Liste der Plätze, damit wir sie als Tabelle
            # darstellen können:
            return zip_longest(*platzlisten)
        else:
            return []


    @staticmethod
    def aktuelle_bloecke(verwaltungszeitraum):
        return verwaltungszeitraum.bloecke.order_by('name')


class EmailPreview(View):
    def post(self, request):
        """
        Erstellt eine Vorschau der übergebenen Vorlage.
        Dazu wählen wir zufällig einen Studenten des aktuellen
        Verwaltungszeitraums aus, rendern die Vorlage mit diesen Daten und geben
        das Ergebnis zurück.
        """
        akt_verw_zr = request.user.mitarbeiter.akt_verw_zeitraum
        student = Student.objects.filter(
            verwaltungszeitraum=akt_verw_zr
        ).order_by('?').first()

        try:
            platz = student.platz
        except Platz.DoesNotExist:
            platz = None

        try:
            vorlagen_text = Template(request.POST.get('content', ''))
        except TemplateSyntaxError:
            vorlagen_text = Template('In der Vorlage ist ein Syntaxfehler!')

        context = Context({'student': student, 'platz': platz})
        preview = vorlagen_text.render(context)

        return HttpResponse(preview)
