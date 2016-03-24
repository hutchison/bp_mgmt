from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import VorlagenDetail


urlpatterns = [
    url(r'^vorlage/(?P<token>[-\w]+)/$', VorlagenDetail.as_view(), name='vorlage'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
