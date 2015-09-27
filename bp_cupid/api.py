from django.conf.urls import url

from rest_framework import serializers, generics
from rest_framework.urlpatterns import format_suffix_patterns

from bp_cupid.models import Vorlage


class VorlagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vorlage
        fields = ('token', 'text')
        read_only_fields = ('token', )


class VorlagenDetail(generics.RetrieveAPIView):
    queryset = Vorlage.objects.all()
    serializer_class = VorlagenSerializer
    lookup_field = 'token'


urlpatterns = [
    url(r'^vorlage/(?P<token>[-\w]+)/$', VorlagenDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
