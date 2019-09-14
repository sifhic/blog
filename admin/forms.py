from django import forms
from django.utils.translation import ugettext_lazy as _
from blog.models import SiteProfile


class SiteProfileForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}))

    class Meta:
        model = SiteProfile
        exclude = []

    def __init__(self, *args, **kwargs):
        super(SiteProfileForm, self).__init__(*args, **kwargs)
