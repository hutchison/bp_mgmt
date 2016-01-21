from bp_cupid.views.index import index
from bp_cupid.views.status import status
from bp_cupid.views.gewichte import gewichte
from bp_cupid.views.studenten import studenten
from bp_cupid.views.student import student
from bp_cupid.views.praxen import praxen
from bp_cupid.views.praxis import praxis
from bp_cupid.views.plaetze import plaetze
from bp_cupid.views.platzuebersicht import platzuebersicht
from .verteilen import (
    zufaellig_verteilen,
    gezielt_verteilen,
)
from bp_cupid.views.studenten_zulassen import studenten_zulassen
from bp_cupid.views.bloecke import bloecke
from bp_cupid.views.email import email, preview_email
from bp_cupid.views.zusatzinfo import zusatzinfo
from bp_cupid.views.pdf import praxis as pdf_praxis
from bp_cupid.views.pdf import praxen as pdf_praxen
from bp_cupid.views import excel
from .einstellungen import einstellungen
