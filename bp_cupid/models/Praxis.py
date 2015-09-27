"""
Eine Praxis.
"""

from django.db import models
try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model
from django.utils.http import urlquote
from bp_cupid.models import (
    Landkreis,
    Zeitraum,
    Block,
)
from operator import attrgetter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.platypus.tables import Table
from reportlab.lib.pagesizes import A4
from io import BytesIO


class PraxisManager(models.Manager):
    """
    Besondere Funktionen für alle Praxen.
    """
    def frei(self):
        return [p for p in self.all() if p.freie_zeitraeume.exists()]


class Praxis(models.Model):
    """
    Eine Praxis liegt in einem Landkreis und bietet Zeiträume an, in denen
    Blockpraktikanten angenommen werden. Weiterhin besitzt sie einige
    persönliche und BP-relevante Daten.
    """
    # Relationen
    landkreis = models.ForeignKey(
        Landkreis,
        null=True,
        related_name='praxen',
    )
    zeitraeume = models.ManyToManyField(
        Zeitraum,
        db_table='praxis_zeitraum',
        verbose_name='Zeiträume',
        blank=True,
        related_name='praxen',
    )
    freie_zeitraeume = models.ManyToManyField(
        Zeitraum,
        db_table='praxis_zeitraum_frei',
        verbose_name='freie Zeiträume',
        blank=True,
        related_name='praxen_frei',
    )
    belegte_zeitraeume = models.ManyToManyField(
        Zeitraum,
        db_table='praxis_zeitraum_belegt',
        verbose_name='belegte Zeiträume',
        blank=True,
        related_name='praxen_belegt',
    )

    objects = PraxisManager()

    # persönliche Daten
    anrede = models.CharField(max_length=15, blank=True, default='')
    vorname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100, blank=True)
    plz = models.IntegerField(default=0)
    ort = models.CharField(max_length=50, blank=True, default='')
    telefon = models.CharField(max_length=20, blank=True, default='')
    telefax = models.CharField(max_length=20, blank=True, default='')
    homepage = models.URLField(blank=True, default='')
    email = models.EmailField(blank=True, default='')

    # BP-relevante Daten
    unterkunft = models.CharField(
        max_length=100,
        blank=True,
        default=''
    )
    lehre_bp = models.BooleanField(
        default=False,
        verbose_name='BP'
    )
    lehre_pj = models.BooleanField(
        default=False,
        verbose_name='PJ'
    )
    kinder = models.BooleanField(
        default=False,
        verbose_name='Kinder/Jugendliche'
    )
    sono = models.BooleanField(
        default=False,
        verbose_name='Sonografie'
    )
    sport = models.BooleanField(
        default=False,
        verbose_name='Sportmedizin'
    )
    kompl = models.BooleanField(
        default=False,
        verbose_name='Komplementärmedizin'
    )
    freie_unterkunft = models.BooleanField(
        default=False,
        verbose_name='freie UK?',
        help_text='freie Unterkunft',
    )
    billige_unterkunft = models.BooleanField(
        default=False,
        verbose_name='billige UK?',
        help_text='billige Unterkunft',
    )
    nur_mit_auto = models.BooleanField(
        default=False,
        verbose_name='nur Auto',
        help_text='nur mit Auto erreichbar?',
    )
    erg_taetigkeiten = models.TextField(
        blank=True,
        verbose_name='Ergänzungen zu den abgefragten Tätigkeitsschwerpunkten'
    )
    andere_kriterien = models.TextField(
        blank=True,
        verbose_name='andere Kriterien'
    )
    erg_unterbringung = models.TextField(
        blank=True,
        verbose_name='Ergänzungen zu den Angaben zur Unterbringung')
    sonstiges = models.TextField(
        blank=True,
        verbose_name='Sonstiges'
    )

    def sortierte_zeitraeume(self):
        """
        Gibt die angebotenen Zeiträume sortiert zurück.
        """
        return self.zeitraeume.order_by('anfang')

    def anzahl_zeitraeume(self):
        """
        Gibt die Anzahl der Zeiträume zurück.
        """
        return self.zeitraeume.count()

    def erster_freier_zeitraum(self):
        """
        Gibt den ersten freien Zeitraum der Praxis zurück. Falls alle Zeiträume
        belegt sind, wird None zurückgegeben.
        """
        return self.freie_zeitraeume.first()

    def aktualisiere_zeitraeume(self):
        """
        Organisiert die freien und belegten Zeiträume.

        Alle direkt und indirekt belegten Zeiträume kommen in
        belegte_zeitraeume; alle angebotenen Zeiträume, die nicht belegt sind,
        kommen in freie_zeitraeume.

        Dabei kann ein Zeitraum "belegt" sein, selbst wenn dieser von der Praxis
        gar nicht angeboten wird (weil er indirekt belegt wird).
        """
        # erstmal aufräumen:
        for zr in self.freie_zeitraeume.all():
            self.freie_zeitraeume.remove(zr)
        for zr in self.belegte_zeitraeume.all():
            self.belegte_zeitraeume.remove(zr)

        # erst die belegten:
        for platz in self.plaetze.all():
            ueberl_zr = platz.zeitraum.ueberlappende_zeitraeume()
            for ue_zr in ueberl_zr:
                self.belegte_zeitraeume.add(ue_zr)

        # dann die freien:
        for zr in self.zeitraeume.all():
            if zr not in self.belegte_zeitraeume.all():
                self.freie_zeitraeume.add(zr)

    def bloecke(self):
        """
        Gibt die Blöcke zurück, in denen die Praxis Zeiträume anbietet.
        """
        return set(z.block for z in self.zeitraeume.select_related('block'))

    def anzahl_bloecke(self):
        """
        Gibt die Anzahl der Blöcke zurück.
        """
        return len(self.bloecke())

    def freie_zeitraeume_in_block(self, block):
        """
        Gibt die freien Zeiträume der Praxis vom übergebenen Block zurück.
        """
        block_zeitraeume = block.zeitraeume.all()
        return sorted(
            set(self.freie_zeitraeume.all()) & set(block_zeitraeume),
            key=attrgetter('anfang'),
        )

    def hat_platz_in_block(self, block):
        """
        Gibt an, ob die Praxis in diesem Block noch freie Zeiträume hat.
        """
        return bool(self.freie_zeitraeume_in_block(block))

    def voll_belegt(self):
        """
        Gibt an, ob die Praxis schon voll belegt ist.
        """
        return not self.freie_zeitraeume.exists()

    def kapazitaet(self, block):
        """
        Gibt die Kapazität der Praxis vom übergebenen Block zurück.
        """
        k = 0
        ueberl = set()

        for zeitr in block.zeitraeume.all():
            if zeitr in self.zeitraeume.all() and zeitr not in ueberl:
                k += 1
                ueberl.update(zeitr.ueberlappende.all())

        return k

    def maximale_kapazitaet(self):
        """
        Gibt die maximale Kapazität der Praxis zurück.
        """
        return sum(self.kapazitaet(b) for b in Block.objects.all())

    def maps_link(self):
        """
        Gibt einen Link zu Google Maps zurück.
        """
        maps_url = 'https://www.google.de/maps/place/'
        return maps_url + urlquote(
                self.adresse + ' '
                + str(self.plz) + ' '
                + self.ort
        )

    def pdf_elemente(self, verwaltungszeitraum):
        """
        Erzeugt eine Liste von Elementen für die Erstellung der PDF-Übersicht
        mit ReportLab.
        """

        # anfangs richten wir unsere Stylesheets ein:
        styles = getSampleStyleSheet()
        styleH1 = styles['Heading1']
        styleH2 = styles['Heading2']
        styleN = styles['BodyText']
        styleN.spaceAfter = 6

        """
        Für die PDF-Übersicht brauchen wir eine Liste von Elementen aus dem
        Fundus von ReportLab. Wir legen die Liste an und befüllen sie mit den
        ersten Überschriften und Absätzen.
        """
        elements = []
        elements.append(Paragraph('Einteilung des Blockpraktikums', styleH1))
        par_einteilung = """
        Für die Praxis von {praxis.anrede} {praxis.name} wurden
        im Verwaltungszeitraum {verw_zr.name} folgende Studenten eingeteilt:
        """
        par_einteilung = par_einteilung.format(
            praxis=self,
            verw_zr=verwaltungszeitraum
        )
        par_einteilung = par_einteilung.replace('Herr', 'Herrn')
        elements.append(Paragraph(par_einteilung, styleN))

        # die Platztabelle ist intern nur eine Liste von Tupeln:
        plaetze = [
            # Überschriften:
            (
                Paragraph('<b>Beginn</b>', styleN),
                Paragraph('<b>Ende</b>', styleN),
                Paragraph('<b>Name</b>', styleN)
            )
        ] + [
            # die eigentlichen Plätze:
            (
                p.zeitraum.anfang.strftime("%d.%m.%Y"),
                p.zeitraum.ende.strftime("%d.%m.%Y"),
                p.student.vorname + " " + p.student.name,
            )
            for p in self.plaetze.filter(
                zeitraum__block__verwaltungszeitraum=verwaltungszeitraum
            ).order_by('zeitraum')
        ]
        tab_plaetze = Table(plaetze, style=[
            ('LINEABOVE', (0, 1), (-1, 1), 1, (0, 0, 0))]
        )
        elements.append(tab_plaetze)

        """
        Die Zusatzinformationen werden nur hinzugefügt, wenn sie auch
        existieren und der Text nicht leer ist.
        """
        ZusatzinfoPraxis = get_model('bp_cupid', 'ZusatzinfoPraxis')
        try:
            zusatzinfo = self.zusatzinfopraxis_set.get(
                verwaltungszeitraum=verwaltungszeitraum
            )
            if zusatzinfo.text:
                elements.append(Paragraph('Zusatzinformationen', styleH2))
                for par in zusatzinfo.text.splitlines():
                    if par:
                        elements.append(Paragraph(par, styleN))
        except ZusatzinfoPraxis.DoesNotExist:
            pass

        return elements

    def pdf(self, verwaltungszeitraum):
        """
        Erzeugt die PDF-Übersicht der Praxis. Gibt die reinen Bytes zurück.
        """
        elements = self.pdf_elemente(verwaltungszeitraum=verwaltungszeitraum)
        with BytesIO() as buf:
            doc = SimpleDocTemplate(buf, pagesize=A4)
            doc.build(elements)
            pdf_content = buf.getvalue()
        return pdf_content

    class Meta:
        verbose_name = 'Praxis'
        verbose_name_plural = 'Praxen'

    def __str__(self):
        return '%s %s (%s)' % (self.vorname, self.name, self.id)
