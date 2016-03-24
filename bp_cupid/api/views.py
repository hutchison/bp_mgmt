from rest_framework import generics

from .serializers import VorlagenSerializer

from ..models import Vorlage


class VorlagenDetail(generics.RetrieveAPIView):
    queryset = Vorlage.objects.all()
    serializer_class = VorlagenSerializer
    lookup_field = 'token'
