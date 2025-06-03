from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('esp32/data/', views.esp32_data, name='esp32_data'),
    path('upload_fingerprint/', views.upload_fingerprint, name='upload_fingerprint'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
