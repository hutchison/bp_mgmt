from rest_framework import serializers

from ..models import Vorlage

class VorlagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vorlage
        fields = ('token', 'text')
        read_only_fields = ('token', )
