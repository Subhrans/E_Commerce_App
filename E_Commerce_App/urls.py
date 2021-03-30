from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.contrib.auth import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('E_Commerce.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)