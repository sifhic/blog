__author__ = 'brian'
from kenyans_github import views
from django.conf.urls import url,include

from datetime import datetime

urlpatterns = [
    url(r'^$',views.setup),
    url(r'^api/',include(
        [
        #url(r'^$', views.index, name='index'),
        url(r'^activities/$', views.index, name='index'),
        ]),
        name='kenyans_on_github'),
]
