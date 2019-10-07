from django import forms
from django.utils.translation import ugettext_lazy as _
from nt.models import Config


class ConfigForm(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}))

    class Meta:
        model = Config
        exclude = ['site']

    def __init__(self, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)


class SyncPostForm(forms.Form):
    url = forms.CharField(widget=forms.URLInput(attrs={'placeholder': 'View As Page Url'}))