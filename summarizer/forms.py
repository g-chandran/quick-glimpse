from django import forms
from django.forms.forms import Form
from django.forms.widgets import FileInput


class InputDataForm(forms.Form):
    enter_text = forms.CharField(widget=forms.Textarea, required=False)
    enter_url = forms.CharField(max_length=500, required=False)
    enter_file = forms.FileField(
        required=False, widget=FileInput(attrs={'accept': 'text/plain'}))
