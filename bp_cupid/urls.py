from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from bp_cupid import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^status/$', views.status, name='status'),
    url(r'^gewichte/$', views.gewichte, name='gewichte'),
    url(r'^studenten/$', views.studenten, name='studenten'),
    url(r'^student/(?P<mat_nr>\d+)/$', views.student, name='student'),
    url(r'^praxen/$', views.praxen, name='praxen'),
    url(r'^praxis/(?P<praxis_id>\d+)/$', views.praxis, name='praxis'),
    url(r'^plaetze/$', views.plaetze, name='plaetze'),
    url(r'^platzuebersicht/$', views.platzuebersicht, name='platzuebersicht'),
    url(r'^verteilen/$', views.verteilen, name='verteilen'),
    url(r'^zulassen/$', views.studenten_zulassen, name='studenten_zulassen'),
    url(r'^bloecke/$', views.bloecke, name='bloecke'),
    url(r'^email/$', views.email, name='email'),
    url(r'^email/preview/$', views.preview_email, name='preview_email'),
    url(r'^zusatzinfo/$', views.zusatzinfo, name='zusatzinfo'),
    url(r'^pdf/praxis/(?P<praxis_id>\d+)/$', views.pdf.praxis, name='pdf_praxis'),
    url(r'^pdf/praxen/$', views.pdf.praxen, name='pdf_praxen'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
