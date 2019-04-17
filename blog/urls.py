from . import views
from django.conf.urls import url,include
from django.urls import path


app_name = 'blog'

urlpatterns = [
    url(r'^$', views.post_list, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^contact_me/$', views.send_email, name='contact_me'),
    url(r'^categories/', include(([
        url(r'^$', views.category_list, name='list'),
        url(r'^create', views.category_create, name='create'),
        # url(r'^(?P<slug>[-\w\d]+)/', include(([
        #
        # ],'category'))),
    ],'categories'))),

    url(r'^posts/', include(([
        url(r'^$', views.post_list, name='list'),
        url(r'^create', views.post_create, name='create'),

        url(r'^(?P<post_pk>\d+)/', include(([
            url(r'^$', views.post_view, name='view'),
            url(r'^(?P<slug>[-\w\d]+)', views.post_view, name='view-slug'),

            url(r'comment/$', views.comment, name='comment'),
            # path('<slug:slug>/', views.post, name='post'),
            #url(r'^(?P<pk>\d+)/$', views.groups_detail, name='detail'),
            url(r'^edit$', views.post_edit, name='edit'),
            url(r'^delete$', views.post_delete, name='delete')
        ],'post'))),
    ],'posts'))),

]
