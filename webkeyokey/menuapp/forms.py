from django import forms
from main.models import Option, EtcOption

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['takeout', 'count']

class EtcOptionForm(forms.ModelForm):
    class Meta:
        model = EtcOption
        fields = ['option_name']
        widgets = {
            'option_name': forms.Select()
        }