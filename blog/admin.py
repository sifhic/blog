from django.contrib import admin
from blog.models import Post,Comment
from django.db import models
from django.forms import ModelForm
from django.contrib.admin import ModelAdmin

# Register your models here.

class CommentAdmin(admin.StackedInline):
    model = Comment
    extra = 1

class PostForm(ModelForm):
    class Meta:
        #model = Post
        _ck_editor_toolbar = [
                {'name': 'basicstyles', 'groups': ['basicstyles', 'cleanup']},
                {'name': 'paragraph',
                 'groups': ['list', 'indent', 'blocks', 'align']},
                {'name': 'document', 'groups': ['mode']}, '/',
                {'name': 'styles'}, {'name': 'colors'},
                {'name': 'insert_custom',
                 'items': ['Image', 'Flash', 'Table', 'HorizontalRule']},
                {'name': 'about'}]
    
        _ck_editor_config = {'autoGrow_onStartup': True,
                             'autoGrow_minHeight': 100,
                             'autoGrow_maxHeight': 250,
                             'extraPlugins': 'autogrow',
                             'toolbarGroups': _ck_editor_toolbar}
        
        # widgets = {
        #     'body': CKEditorWidget(editor_options=_ck_editor_config)
        # }


class PostAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('heading',)}
    form=PostForm
    fieldsets = [
        ('Post Meta',{
            'fields':['creator']
            }),
        (None,  {'fields' : ['heading','sub_heading','is_published']}),
        ('Post Body',{
            'classes': ('grp-collapse grp-closed',),
            'fields':['body']
            }),
        ('Featured Image',{'fields':['featured_image']}),

    ]
    inlines = [CommentAdmin]
    list_filter = ['created_at']
    search_fields = ['body']

admin.site.register(Post,PostAdmin)