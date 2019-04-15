from django.conf.urls import include, url
from django.conf import settings
from django.urls import path

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = [
    path('', include('authentication.urls')),
    path('', include('blog.urls')),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    #url(r'^newsletter/', include('newsletter.urls')),
    path('admin/', include('admin.urls')),
    #path('admin_django/', admin.site.urls),

]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
