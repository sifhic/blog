from django.contrib import admin
from blog.models import Post,Comment

# Register your models here.

class CommentAdmin(admin.StackedInline):
    model = Comment
    extra = 1


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('creator',{'fields':['creator']}),
        (None,  {'fields' : ['heading','body']}),
        ('Date Info',{'fields':['pub_date'],'classes':['collapse']})
    ]
    inlines = [CommentAdmin]
    list_filter = ['pub_date']
    search_fields = ['body']

admin.site.register(Post,PostAdmin)