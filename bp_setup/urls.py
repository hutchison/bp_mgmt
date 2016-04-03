from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from bp_setup import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^fragebogen/$', views.Fragebogen.as_view(), name='fragebogen'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
