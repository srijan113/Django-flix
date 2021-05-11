from django import forms
from django.forms.forms import Form
from django.forms.widgets import HiddenInput
from .models import RatingChoices

class RatingForm(forms.Form):
    rating = forms.ChoiceField(label="",choices=RatingChoices.choices)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content_type_id = forms.IntegerField(widget=forms.HiddenInput)
    next = forms.CharField(widget=forms.HiddenInput)
