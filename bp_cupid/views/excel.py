from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.utils.http import urlquote

from io import BytesIO
import xlsxwriter

from ..models import (
    Verwaltungszeitraum,
    Block,
    Zeitraum,
    Platz,
)
from .Platzuebersicht import platztabelle

@login_required
@user_passes_test(lambda u: u.is_staff)
def platzuebersicht(request, verwzr_id):
    """Gibt eine Exceltabelle der Platzübersicht des übergebenen
    Verwaltungszeitraums zurück.
    """

    verwzr = Verwaltungszeitraum.objects.get(id=verwzr_id)
    bloecke = verwzr.bloecke.order_by('name')
    zeitraeume = Zeitraum.objects.filter(block__in=bloecke).order_by('anfang')

    buf = BytesIO()
    with xlsxwriter.Workbook(buf, {'in_memory': True}) as workbook:
        ws = workbook.add_worksheet()

        # Ganz links oben steht 'Praxis':
        ws.merge_range(
            0, 0,
            1, 0,
            'Praxis'
        )

        # Die Blöcke belegen die erste Zeile. Dabei nehmen sie so viele Zellen
        # ein, wie sie Zeiträume besitzen.
        b = 1
        for block in bloecke:
            zc = block.zeitraeume.count()
            ws.merge_range(
                0, b,
                0, b+zc-1,
                block.name
            )
            b += zc

        # Die Zeiträume belegen die zweite Zeile. Ein Zeitraum pro Zelle.
        z = 1
        for zeitraum in zeitraeume:
            ws.write(
                1, z,
                '{} – {}'.format(
                    zeitraum.anfang.strftime('%d.%m.%Y'),
                    zeitraum.ende.strftime('%d.%m.%Y'),
                )
            )
            z += 1

        """
        Die Platztabelle.

        Eine Praxis hat dabei zwei Zeilen. Der Name der Praxis erstreckt sich
        über zwei Zellen. Falls ein Platz auftaucht, schreiben wir die
        Platzinfos in zwei Zellen. In die obere kommen Name und Matrikelnummer
        und in die untere kommt die E-Mail-Adresse als Link.
        """
        pl_tab = platztabelle(zeitraeume)
        y = 2
        for praxis in pl_tab:
            x = 0
            ws.merge_range(
                y, x,
                y+1, x,
                '{} {}'.format(praxis.vorname, praxis.name)
            )

            # Die Platzbegrenzung bekommen dazu, jedoch brauchen wir sie nicht.
            # Daher lassen wir das letzte Element weg.
            belegungen = pl_tab[praxis][:-1]
            for eintrag in belegungen:
                x += 1
                if type(eintrag) == Platz:
                    student = eintrag.student
                    ws.write(y, x, str(student))
                    ws.write_url(y+1, x, 'mailto:{}'.format(student.email))
            y += 2

    dateiname = 'Platzübersicht {}.xlsx'.format(verwzr.name)
    buf.seek(0)
    response = HttpResponse(
        buf.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = """attachment;\
        filename="{0}";\
        filename*=UTF-8''{0};\
    """.format(urlquote(dateiname))

    return response
