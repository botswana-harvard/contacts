from django import forms


class ContactSearchForm(forms.Form):

    search_value = forms.CharField(
        label = "",
        max_length=200)
