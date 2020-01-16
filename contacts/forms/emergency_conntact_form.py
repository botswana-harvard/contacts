from django import forms

from ..models import EmergencyContact


class EmergencyContactForm(forms.ModelForm):

    class Meta:
        model = EmergencyContact
        fields = '__all__'
