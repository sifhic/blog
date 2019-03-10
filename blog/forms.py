__author__ = 'brian'

from django import forms
from django.utils.translation import ugettext_lazy as _
from blog.models import Post,Category


class PostForm(forms.ModelForm):
    # link = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Invite or .me Link'}))
    # accounts = forms.ModelMultipleChoiceField(
    #     queryset=Account.objects.filter(status=Account.READY),
    #     required=True
    # )

    class Meta:
        model = Post
        exclude = ['creator','created_at','updated_at','slug','site']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # self.fields["accounts"].initial = (
        #     Account.objects.free().values_list(
        #         'id', flat=True
        #     )
        # )


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        exclude = ['created_at','updated_at','site','slug']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
