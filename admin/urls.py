from . import views
from django.conf.urls import url, include
from django.urls import path

app_name = 'admin'

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^posts/', include(
        ([
             url(r'^$', views.post_list, name='list'),
             # url(r'^create', views.post_create, name='create'),
             # url(r'^(?P<slug>[-\w\d]+)/', include(
             #     ([
             #          url(r'^$', views.post_view, name='view'),
             #          url(r'comment/$', views.comment, name='comment'),
             #      ], 'post'))),
         ], 'posts'))),

    url(r'^categories/', include(
        ([
             url(r'^$', views.category_list, name='list'),
             # url(r'^create', views.post_create, name='create'),
             # url(r'^(?P<slug>[-\w\d]+)/', include(
             #     ([
             #          url(r'^$', views.post_view, name='view'),
             #          url(r'comment/$', views.comment, name='comment'),
             #      ], 'post'))),
         ], 'categories'))),
    url(r'^media/', include(
        ([

             url(r'^$', views.media_list, name='list'),

         ], 'media'))),
    url(r'^users/', include(
        ([
             url(r'^$', views.users_list, name='list'),

         ], 'users'))),
    url(r'^settings/', include(
        ([
             url(r'^$', views.settings_list, name='list'),

         ], 'settings')))

]
