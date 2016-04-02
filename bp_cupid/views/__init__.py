from bp_cupid.views.index import index
from bp_cupid.views.Status import Status
from bp_cupid.views.gewichte import gewichte
from bp_cupid.views.Studenten import Studenten
from bp_cupid.views.student import student
from bp_cupid.views.Praxen import Praxen
from bp_cupid.views.praxis import praxis
from bp_cupid.views.Plaetze import Plaetze
from bp_cupid.views.Platzuebersicht import Platzuebersicht
from .verteilen import (
    zufaellig_verteilen,
    gezielt_verteilen,
)
from bp_cupid.views.studenten_zulassen import studenten_zulassen
from bp_cupid.views.Bloecke import Bloecke
from bp_cupid.views.email import email, preview_email
from bp_cupid.views.zusatzinfo import zusatzinfo
from bp_cupid.views.pdf import praxis as pdf_praxis
from bp_cupid.views.pdf import praxen as pdf_praxen
from bp_cupid.views import excel
from .einstellungen import einstellungen
from .Evaluation import EvaluationList, EvaluationDetail
