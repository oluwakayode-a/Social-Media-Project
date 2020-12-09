from .models import Suggestion, Report
from django import forms

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        exclude = ['user']


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        exclude = ['user', 'post']