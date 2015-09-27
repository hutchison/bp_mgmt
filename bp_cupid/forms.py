from django import forms
from django_ace import AceWidget

from .models import Vorlage


class VorlagenForm(forms.ModelForm):
    class Meta:
        model = Vorlage
        fields = ['token', 'text']
        widgets = {
            'text': AceWidget(
                mode='django',
                theme='solarized_light',
                width='900px',
                height='400px',
                wordwrap=True,
            ),
        }
