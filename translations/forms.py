from django import forms
from translations.models import TransUnit

EMPTY_ITEM_ERROR = "You can't submit empty string"

class TMForm(forms.models.ModelForm):
    class Meta:
        model = TransUnit
        fields = ('source', 'target')
        widgets = {
        'source': forms.fields.TextInput(
            attrs={
            'placeholder': "Enter source text", 
            'class' : "form-control",
            }),
        'target' :forms.fields.TextInput(
            attrs={
            'placeholder': "Enter target text", 
            'class' : "form-control",
            })
            } 
        error_messages = {
        'source': {'required': EMPTY_ITEM_ERROR},
        'target': {'required': EMPTY_ITEM_ERROR}
        }
        