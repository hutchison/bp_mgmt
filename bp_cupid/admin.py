from django.contrib import admin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.http import urlencode

from simple_history.admin import SimpleHistoryAdmin

from .models import (
    Block,
    Evaluation,
    Gewicht,
    Landkreis,
    Mitarbeiter,
    Platz,
    Platzbegrenzung,
    Praxis,
    Student,
    Verwaltungszeitraum,
    Vorlage,
    Zeitraum,
    ZusatzinfoPraxis,
)
from .forms import VorlagenForm


@admin.register(Landkreis)
class LandkreisAdmin(admin.ModelAdmin):
    list_display = ('name', 'plz_von', 'plz_bis', 'orte')
    list_display_links = ('name',)
    ordering = ('plz_von',)


@admin.register(Verwaltungszeitraum)
class VerwaltungszeitraumAdmin(admin.ModelAdmin):
    list_display = ('name', 'anfang', 'ende')
    ordering = ('anfang', )


@admin.register(Platz)
class PlatzAdmin(SimpleHistoryAdmin):
    list_display = ('student', 'praxis', 'zeitraum', 'manuell', 'kommentar')
    ordering = ('student__name', )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        praxis_id = request.GET.get('praxis', None)
        zeitraum_id = request.GET.get('zeitraum', None)
        manuell = request.GET.get('manuell', False)

        if praxis_id and zeitraum_id:
            Platz.objects.get(student=object_id).delete()
            d = {
                'student': object_id,
                'praxis': praxis_id,
                'zeitraum': zeitraum_id,
                'manuell': manuell,
            }
            return redirect(
                '%s?%s' % (
                    reverse('admin:bp_cupid_platz_add'),
                    urlencode(d)
                )
            )
        else:
            return super(PlatzAdmin, self).change_view(
                request, object_id, form_url, extra_context=extra_context
            )
    search_fields = ['student__vorname', 'student__name', 'student__mat_nr']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'mat_nr',
        'vorname', 'name',
        'weiblich',
        'verwaltungszeitraum',
        'gewichtung_kinder',
        'gewichtung_sono',
        'gewichtung_sport',
        'gewichtung_kompl',
        'gewichtung_hohe_duene',
        'fs_und_fahrzeug',
        'priv_unterkunft',
        'adresse_priv_unterkunft',
        'sonstiges',
        'extern',
        'hat_fragebogen_ausgefuellt',
    )
    list_editable = ('weiblich', 'verwaltungszeitraum')
    filter_horizontal = (
        'landkreise',
        'bevorzugte_praxen',
        'abgeneigte_praxen',
    )
    search_fields = ['vorname', 'name', 'mat_nr']


@admin.register(Zeitraum)
class ZeitraumAdmin(admin.ModelAdmin):
    list_display = ('block', 'anfang', 'ende')
    list_display_links = ('anfang',)
    readonly_fields = ('ueberlappende',)
    ordering = ('anfang',)


class ZeitraumInline(admin.TabularInline):
    model = Zeitraum
    readonly_fields = ('ueberlappende',)
    extra = 1


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('name', 'verwaltungszeitraum', 'zeiten')
    ordering = ('name',)
    inlines = [
        ZeitraumInline,
    ]


class PlatzbegrenzungInline(admin.TabularInline):
    model = Platzbegrenzung
    extra = 1


@admin.register(Praxis)
class PraxisAdmin(admin.ModelAdmin):
    list_display = (
        'anrede',
        'vorname',
        'name',
        'ist_aktiv',
        'hat_didaktikschulung_besucht',
        'landkreis',
        'lehre_bp',
        'lehre_pj',
        'kinder',
        'sono',
        'sport',
        'kompl',
        'erg_taetigkeiten',
        'andere_kriterien',
        'nur_mit_auto',
        'freie_unterkunft',
        'billige_unterkunft',
        'unterkunft',
        'erg_unterbringung',
        'sonstiges',
    )
    list_display_links = ('name',)
    readonly_fields = ('freie_zeitraeume', 'belegte_zeitraeume')
    list_editable = ('ist_aktiv', 'hat_didaktikschulung_besucht')
    ordering = ('name',)
    filter_horizontal = ('zeitraeume', 'freie_zeitraeume', 'belegte_zeitraeume')
    search_fields = ['vorname', 'name']
    inlines = [
        PlatzbegrenzungInline,
    ]


@admin.register(Gewicht)
class GewichtAdmin(admin.ModelAdmin):
    list_display = ('student', 'praxis', 'wert', 'umgebrochener_kommentar')
    ordering = ('student', 'praxis')
    search_fields = ['student__vorname', 'student__name', 'student__mat_nr']


@admin.register(Mitarbeiter)
class MitarbeiterAdmin(admin.ModelAdmin):
    list_display = ('user', 'akt_verw_zeitraum')
    list_editable = ('akt_verw_zeitraum', )


@admin.register(Vorlage)
class VorlagenAdmin(admin.ModelAdmin):
    list_display = ('token', 'text')
    ordering = ('token', )
    form = VorlagenForm
    search_fields = ['token', 'text']


@admin.register(ZusatzinfoPraxis)
class ZusatzinfoPraxisAdmin(admin.ModelAdmin):
    list_display = ('praxis', 'verwaltungszeitraum', 'text')
    list_display_links = ('praxis',)
    ordering = ('-verwaltungszeitraum__anfang', 'praxis')
    search_fields = ['praxis', 'text']


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('platz', 'eval_user', 'datum')
    list_display_links = ('platz', )
    readonly_fields = ('datum',)
    search_fields = [
        'platz__student__vorname',
        'platz__student__name',
        'platz__student__mat_nr',
        'platz__praxis__vorname',
        'platz__praxis__name',
    ]
    ordering = ('-datum', 'platz__student__name')
