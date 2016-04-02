from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from . import views
from . import api

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(regex=r'^api/', view=include(api.urls, namespace='api')),
    url(r'^status/$', views.Status.as_view(), name='status'),
    url(r'^einstellungen/$', views.einstellungen, name='einstellungen'),
    url(r'^gewichte/$', views.gewichte, name='gewichte'),
    url(r'^studenten/$', views.Studenten.as_view(), name='studenten'),
    url(r'^student/(?P<mat_nr>\d+)/$', views.student, name='student'),
    url(r'^praxen/$', views.Praxen.as_view(), name='praxen'),
    url(r'^praxis/(?P<praxis_id>\d+)/$', views.praxis, name='praxis'),
    url(r'^plaetze/$', views.Plaetze.as_view(), name='plaetze'),
    url(r'^platzuebersicht/$', views.platzuebersicht, name='platzuebersicht'),
    url(r'^zufaellig_verteilen/$', views.zufaellig_verteilen, name='zufaellig_verteilen'),
    url(r'^gezielt_verteilen/$', views.gezielt_verteilen, name='gezielt_verteilen'),
    url(r'^zulassen/$', views.studenten_zulassen, name='studenten_zulassen'),
    url(r'^bloecke/$', views.bloecke, name='bloecke'),
    url(r'^email/$', views.email, name='email'),
    url(r'^email/preview/$', views.preview_email, name='preview_email'),
    url(r'^zusatzinfo/$', views.zusatzinfo, name='zusatzinfo'),
    url(r'^pdf/praxis/(?P<praxis_id>\d+)/$', views.pdf.praxis, name='pdf_praxis'),
    url(r'^pdf/praxen/$', views.pdf.praxen, name='pdf_praxen'),
    url(r'^excel/platzuebersicht/(?P<verwzr_id>\d+)$', views.excel.platzuebersicht, name='excel/platzuebersicht'),
    url(r'^evaluation/$', views.EvaluationList.as_view(), name='evaluation_uebersicht'),
    url(r'^evaluation/(?P<mat_nr>\d+)/$', views.EvaluationDetail.as_view(), name='evaluation'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
