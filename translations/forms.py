from django import forms
from translations.models import TransUnit

EMPTY_SOURCE_ERROR = "You can't submit empty source string"
EMPTY_TARGET_ERROR = "You can't submit empty target string"

class TransUnitForm(forms.models.ModelForm):
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
            'placeholder': "Enter translation text", 
            'class' : "form-control",
            })
            } 
        error_messages = {
        'source': {'required': EMPTY_SOURCE_ERROR},
        'target': {'required': EMPTY_TARGET_ERROR}
        }
        