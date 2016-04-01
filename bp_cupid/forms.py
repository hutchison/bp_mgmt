from django.forms import ModelForm, Textarea, NumberInput, Select
from django_ace import AceWidget

from .models import Vorlage, Evaluation


class VorlagenForm(ModelForm):
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


def bootstrap_field(f, **kwargs):
    field = f.formfield(**kwargs)
    if field and type(field.widget) in [Textarea, NumberInput, Select]:
        field.widget.attrs['class'] = 'form-control'
        if f.name.startswith('kommentar_'):
            field.widget.attrs['rows'] = '2'
    if field and type(field.widget) == NumberInput:
        field.widget.attrs['min'] = '1'
        field.widget.attrs['max'] = '6'
    return field


class EvaluationForm(ModelForm):
    formfield_callback = bootstrap_field
    class Meta:
        model = Evaluation
        fields = '__all__'
