"""
Ein Student.
"""

from django.db import models
from bp_cupid.models import Landkreis, Verwaltungszeitraum
from ..validators import telefon_regex
from django.db.models import Q
try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model
from django.core.exceptions import ValidationError
from django.conf import settings


class StudentManager(models.Manager):
    """
    Besondere Funktionen für alle Studenten.
    """
    def frei(self):
        """
        Gibt alle freien Studenten zurück.

        Ein Student hat einen Platz oder nicht. Wenn dieser Student keinen Platz
        hat, absolviert er/sie das BP extern oder nicht.

        Nur wenn er/sie keinen Platz hat und das BP nicht extern absolviert, ist
        er/sie frei.
        """
        return self.filter(
            Q(platz__isnull=True) & Q(extern=False)
        )


class Student(models.Model):
    """
    Ein Student ist einem Verwaltungszeitraum zugeordnet. Ein Student hat
    persönliche Daten wie Matrikelnummer, Name, E-Mail-Adresse und Weiblichkeit.
    Dazu kommen noch die relevanten Daten für das Blockpraktikum (Kinder, Sono,
    etc.). Weiterhin darf sich ein Student bevorzugte Landkreise aussuchen.
    """
    # Relationen
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
    )
    verwaltungszeitraum = models.ForeignKey(Verwaltungszeitraum)
    # Die gehören eigentlich weiter unten hin, aber es ist auch eine Relation:
    landkreise = models.ManyToManyField(
        Landkreis,
        db_table="student_landkreis",
        blank=True,
    )
    bevorzugte_praxen = models.ManyToManyField(
        'bp_cupid.Praxis',
        db_table='bevorzugte_praxen',
        related_name='bevorzugte_praxen',
        blank=True,
    )
    abgeneigte_praxen = models.ManyToManyField(
        'bp_cupid.Praxis',
        db_table='abgeneigte_praxen',
        related_name='abgeneigte_praxen',
        blank=True,
    )

    """
    Wenn wir alle freien Studenten haben möchten, dann könnten wir das entweder
    über eine classmethod lösen oder den Manager überschreiben. Letzteres wird
    empfohlen und wirkt richtig. Siehe auch den obigen StudentManager.
    """
    objects = StudentManager()

    # persönliche Daten:
    mat_nr = models.IntegerField(
        unique=True,
        verbose_name='Matrikelnummer',
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Name',
        default='',
        blank=True,
    )
    vorname = models.CharField(
        max_length=100,
        verbose_name='Vorname',
        default='',
        blank=True,
    )
    email = models.EmailField(
        verbose_name='E-Mail',
        default='',
    )
    weiblich = models.BooleanField(
        default=False,
    )
    telefonnummer = models.CharField(
        max_length=15,
        default='',
        validators=[telefon_regex],
        verbose_name='Telefonnummer',
        blank=True,
    )
    hat_fragebogen_ausgefuellt = models.BooleanField(
        default=False,
        verbose_name='hat Fragebogen ausgefüllt',
    )

    # BP Vorlieben:
    kinder = models.BooleanField(
        verbose_name='Kinder',
        default=False,
    )
    gewichtung_kinder = models.IntegerField(
        default=0,
        verbose_name='G Kinder',
    )
    sono = models.BooleanField(
        verbose_name='Sono',
        default=False,
    )
    gewichtung_sono = models.IntegerField(
        default=0,
        verbose_name='G Sono',
    )
    sport = models.BooleanField(
        verbose_name='Sport',
        default=False,
    )
    gewichtung_sport = models.IntegerField(
        default=0,
        verbose_name='G Sport',
    )
    kompl = models.BooleanField(
        verbose_name='Kompl',
        default=False,
    )
    gewichtung_kompl = models.IntegerField(
        default=0,
        verbose_name='G Kompl',
    )
    hohe_duene = models.BooleanField(
        verbose_name='H. Düne',
        default=False,
    )
    gewichtung_hohe_duene = models.IntegerField(
        default=0,
        verbose_name='G H. Düne',
    )
    entfernte_praxis_wenn_unterkunft = models.BooleanField(
        verbose_name='entf. Praxis',
        default=False,
    )
    fs_und_fahrzeug = models.BooleanField(
        verbose_name='FS+Auto',
        default=False,
    )
    priv_unterkunft = models.BooleanField(
        verbose_name='priv. Unterkunft',
        default=False
    )
    besondere_praxiskriterien = models.TextField(
        verbose_name='besondere Praxiskriterien',
        default='',
        blank=True,
    )
    adresse_priv_unterkunft = models.TextField(
        max_length=300,
        verbose_name='Ort+PLZ',
        default='',
        blank=True
    )
    sonstiges = models.TextField(
        max_length=500,
        verbose_name='Sonstiges',
        default='',
        blank=True
    )
    extern = models.BooleanField(
        default=False,
        verbose_name='macht BP extern',
    )

    def gewaehlte_landkreise(self):
        """
        Wählt alle gewählten Landkreise, sortiert sie und gibt sie umgebrochen
        aus.
        """
        lks = self.landkreise.all()
        lks = sorted(map(str, lks))
        return '<br />'.join(lks)
    gewaehlte_landkreise.short_description = 'Landkreise'
    gewaehlte_landkreise.allow_tags = True

    def anzahl_landkreise(self):
        return self.landkreise.count()
    anzahl_landkreise.short_description = '#LK'

    def sortierte_gewichte(self):
        """
        Gibt die Gewichte zu den einzelnen Praxen nach Wert sortiert zurück.
        """
        return self.gewichte.order_by('-wert')

    def hat_platz(self):
        Platz = get_model('bp_cupid', 'Platz')
        try:
            return bool(self.platz)
        except Platz.DoesNotExist:
            return False

    def clean(self):
        if self.hat_platz() and self.extern:
            raise ValidationError(
                u'Ein Student darf nicht einen Platz haben und gleichzeitig ' +
                u'das BP extern absolvieren.'
            )

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Studenten'
        ordering = ['name', 'mat_nr']

    def __str__(self):
        return "%s %s (%s)" % (self.vorname, self.name, self.mat_nr)
