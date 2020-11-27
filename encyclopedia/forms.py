from django.forms import ModelForm
from django import forms

# Form for new entries
class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:75%;'}), max_length=100, label="Title")
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 15, 'style': 'width:75%;'}), max_length=800, label="Description")

    # Form for edits
class EditEntryForm(forms.Form):
    title = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'form-control', 'style': 'width:75%;', 'readonly': 'readonly'}), label="Title", required=False)
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 15, 'style': 'width:75%;'}), max_length=800, label="Description", required=False)