__author__ = 'brian'
from . import views
from django.conf.urls import url
from blog.forms import BootstrapAuthenticationForm
from datetime import datetime
import django.contrib.auth.views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^contact_me/$', views.send_email, name='contact_me'),
    url(r'^(?P<post_id>[0-9]+)/$', views.post, name='post'),
    url(r'(?P<post_id>[0-9]+)/comment/$', views.comment, name='comment'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'blog/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
                {
                    'title': 'Log in',
                    'year': datetime.now().year,
                },
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/blog',
        },
        name='logout'),
]
