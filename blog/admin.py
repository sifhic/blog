from django.contrib import admin
from blog.models import Post,Comment
from django.db import models
from tinymce.widgets import TinyMCE
# Register your models here.

class CommentAdmin(admin.StackedInline):
    model = Comment
    extra = 1


class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField:{'widget':TinyMCE(
            attrs={'cols':150,'rows':30},
            mce_attrs={
                'nowrap': True,
                'toolbar': "undo redo | styleselect | bold italic ",
                },
        )}
    }
    fieldsets = [
        ('creator',{'fields':['creator']}),
        (None,  {'fields' : ['heading','body']}),

    ]
    inlines = [CommentAdmin]
    list_filter = ['pub_date']
    search_fields = ['body']

admin.site.register(Post,PostAdmin)