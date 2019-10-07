from nt.views import config_view,sync_view
from django.conf.urls import url, include
from django.urls import path

app_name = 'notion'

urlpatterns = [
    url(r'^$', config_view, name='config'),
    url(r'^sync$', sync_view, name='sync'),

]
