"""
Eine Evaluation.
"""

from django.db import models
from django.conf import settings

from . import Platz


class Evaluation(models.Model):
    class Meta:
        verbose_name = 'Evaluation'
        verbose_name_plural = 'Evaluationen'

    # Relationen
    platz = models.OneToOneField(
        Platz,
        primary_key=True,
        related_name='evaluation'
    )
    eval_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='evaluationen',
        verbose_name='evaluierender Benutzer',
    )

    # eigene Attribute
    datum = models.DateField(
        auto_now_add=True,
        verbose_name='aktuelles Datum',
    )

    positiv = models.TextField(
        default='',
        blank=True,
        help_text='Was war positiv?',
    )
    negativ = models.TextField(
        default='',
        blank=True,
        help_text='Was war negativ?'
    )

    note_lehrarztfaehigkeit = models.DecimalField(
        default=0,
        max_digits=2,
        decimal_places=1,
        verbose_name='Lehrarztfähigkeit des Arztes',
        help_text='Note als Zahl (z.B. 1 oder 2,5)',
    )

    SEHR_ZUFRIEDEN = 1
    ZUFRIEDEN = 2
    MITTELMAESSIG = 3
    UNZUFRIEDEN = 4
    SEHR_UNZUFRIEDEN = 5
    AUSWAHL_ZUFRIEDENHEIT = (
        (SEHR_ZUFRIEDEN, 'sehr zufrieden'),
        (ZUFRIEDEN, 'zufrieden'),
        (MITTELMAESSIG, 'mittelmäßig'),
        (UNZUFRIEDEN, 'unzufrieden'),
        (SEHR_UNZUFRIEDEN, 'sehr unzufrieden'),
    )
    zufriedenheit = models.IntegerField(
        choices=AUSWAHL_ZUFRIEDENHEIT,
        default=MITTELMAESSIG,
        verbose_name='Zufriedenheit mit dem Praktikum',
    )

    note_praktikum = models.DecimalField(
        default=0,
        max_digits=2,
        decimal_places=1,
        verbose_name='Note für das Praktikum',
        help_text='Note als Zahl (z.B. 1 oder 2,5)',
    )

    sonstige_anmerkungen = models.TextField(
        default='',
        blank=True,
        verbose_name='Sonstige Anmerkungen'
    )
    erfahrungen_logbuch = models.TextField(
        default='',
        blank=True,
        verbose_name='Erfahrungen mit dem Logbuch'
    )
    entsprechung_fragebogen = models.TextField(
        default='',
        blank=True,
        verbose_name='Interessen = Fragebogen?',
        help_text='Entspricht der BP-Platz den Interessen wie im' +
        ' Online-Fragebogen angegeben?'
    )

    JA = 1
    NEIN = -1
    KEINE_ANGABE = 0
    AUSWAHL_EIGENSCHAFTEN = (
        (JA, 'ja'),
        (NEIN, 'nein'),
        (KEINE_ANGABE, 'keine Angabe'),
    )

    # typische & relevante Untersuchungstechniken:
    abhoeren_auskultation = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Abhören/Auskultation',
    )
    kommentar_abhoeren_auskultation = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Abhören/Auskultation',
    )
    ohr_untersuchen = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Ohr untersuchen',
    )
    kommentar_ohr_untersuchen = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Ohr untersuchen',
    )
    reflexe_abklopfen = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Reflexe abklopfen',
    )
    kommentar_reflexe_abklopfen = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Reflexe abklopfen',
    )
    bauch_abtasten = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Bauch abtasten',
    )
    kommentar_bauch_abtasten = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Bauch abtasten',
    )
    blutdruck_messen = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Blutdruck messen',
    )
    kommentar_blutdruck_messen = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Blutdruck messen',
    )
    blut_abnehmen = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Blut abnehmen',
    )
    kommentar_blut_abnehmen = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Blut abnehmen',
    )
    blutzucker_messen = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Blutzucker messen',
    )
    kommentar_blutzucker_messen = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Blutzucker messen',
    )
    ekg_schreiben = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='EKG schreiben',
    )
    kommentar_ekg_schreiben = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu EKG schreiben',
    )
    ekg_interpretieren = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='EKG interpretieren',
    )
    kommentar_ekg_interpretieren = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu EKG interpretieren',
    )
    laborbefunde_interpretieren = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Laborbefunde interpretieren',
    )
    kommentar_laborbefunde_interpretieren = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Laborbefunde interpretieren',
    )
    sonstige_untersuchungstechniken = models.TextField(
        default='',
        blank=True,
        verbose_name='sonstige Untersuchungstechniken',
    )

    # Besondere Situationen:

    impfen = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Impfen/Impfberatung',
    )
    kommentar_impfen = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Impfen/Impfberatung',
    )
    spritzen = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Spritzen (z.B. IM, IV, B12, Quaddeln, usw.)',
    )
    kommentar_spritzen = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Spritzen (z.B. IM, IV, B12, Quaddeln, usw.)',
    )
    gesundheits_check_up = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Gesundheits-Check-Up',
    )
    kommentar_gesundheits_check_up = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Gesundheits-Check-Up',
    )
    hausbesuche_pflegeheim = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Hausbesuche/Pflegeheim',
    )
    kommentar_hausbesuche_pflegeheim = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Hausbesuche/Pflegeheim',
    )

    # Praxisorganisation:
    vorbereitung_auf_studenten = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Vorbereitung auf Studenten',
    )
    kommentar_vorbereitung_auf_studenten = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Vorbereitung auf Studenten',
    )
    einbindung_praxisalltag = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Einbindung ins Praxisteam/in Praxisalltag',
    )
    kommentar_einbindung_praxisalltag = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Einbindung ins Praxisteam/in Praxisalltag',
    )
    praxisklima = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Praxisklima',
    )
    kommentar_praxisklima = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Praxisklima',
    )
    eigener_untersuchungsraum = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='eigener Untersuchungsraum',
    )
    kommentar_eigener_untersuchungsraum = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu eigener Untersuchungsraum',
    )

    # Möglichkeiten zur Partizipation/Eigenständigkeit:
    teilnehmen_an_sprechstunde = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='anwesend/teilnehmend in/an Sprechstunde/-zimmer',
    )
    kommentar_teilnehmen_an_sprechstunde = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu anwesend/teilnehmend in/an Sprechstunde/-zimmer',
    )
    aktiv_mituntersucht = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='aktiv mituntersucht',
    )
    kommentar_aktiv_mituntersucht = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu aktiv mituntersucht',
    )
    selbststaendige_untersuchung = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='selbstständige Anamnese/Untersuchung',
    )
    kommentar_selbststaendige_untersuchung = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu selbstständige Anamnese/Untersuchung',
    )

    # Didaktik:
    zeit_raum_fuer_fragen = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Zeit/Raum für Fragen',
    )
    kommentar_zeit_raum_fuer_fragen = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Zeit/Raum für Fragen',
    )
    von_sich_aus_erklaert = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='von sich aus erklärt',
    )
    kommentar_von_sich_aus_erklaert = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu von sich aus erklärt',
    )
    fragen_an_studenten = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Fragen an Studenten',
    )
    kommentar_fragen_an_studenten = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Fragen an Studenten',
    )
    vor_nachbesprechung_der_patienten = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Vor- & Nachbesprechung der Patienten',
    )
    kommentar_vor_nachbesprechung_der_patienten = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Vor- & Nachbesprechung der Patienten',
    )
    motivation = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Motivation des/der LA/LÄ',
    )
    kommentar_motivation = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Motivation des/der LA/LÄ',
    )
    lerneffekt = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Lerneffekt',
    )
    kommentar_lerneffekt = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Lerneffekt',
    )
    feedback_vom_arzt = models.IntegerField(
        choices=AUSWAHL_EIGENSCHAFTEN,
        default=KEINE_ANGABE,
        verbose_name='Feedback vom Arzt',
    )
    kommentar_feedback_vom_arzt = models.TextField(
        default='',
        blank=True,
        verbose_name='Kommentar zu Feedback vom Arzt',
    )

    veraenderungswuensche = models.TextField(
        default='',
        blank=True,
        verbose_name='Veränderungswünsche',
    )
    sonstiges_positiv = models.TextField(
        default='',
        blank=True,
        verbose_name='Sonstiges (positiv)',
    )
    sonstiges_negativ = models.TextField(
        default='',
        blank=True,
        verbose_name='Sonstiges (negativ)',
    )
    sonstiges_neutral = models.TextField(
        default='',
        blank=True,
        verbose_name='Sonstiges (neutral)',
    )

    gesamturteil = models.TextField(
        default='',
        blank=True,
        verbose_name='Gesamturteil',
    )

    def __str__(self):
        return self._meta.verbose_name + ' von ' + str(self.platz)
