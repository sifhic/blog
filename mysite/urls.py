from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from blog import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^blog/',include('blog.urls',namespace='blog')),
    url(r'^$',views.index),
    url(r'^tinymce/',include('tinymce.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
