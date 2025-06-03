"""
URL configuration for biometric project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from biometric_auth import views
from django.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name="home"),
    path('home', views.home,name="home"),
    path('check_pass/', views.check_pass, name='check_pass'),
    path('auth_pass/', views.auth_pass, name='auth_pass'),
    path('finger/', views.finger, name='finger'),
    path('display/', views.display, name='display'),
    path('owner/', views.owner, name='owner'),
    # path('owner_auth/', views.owner_auth, name='owner_auth'),
    
    path('owner_dash/', views.owner_dash, name='owner_dash'),
    path('check_in/', views.check_in, name='check_in'),
    path('check_in/', views.check_in, name='check_in'),
    path('checked/', views.checked, name='checked'),
    path('update_access/', views.update_access, name='update_access'),
    
    path('dash/', views.dash, name='dash'),
    path('see/', views.see, name='see'),
    # path('access_confirm/', views.access_confirm, name='access_confirm'),
    path('members/', include('members.urls')),
    # path("crypto/", include('cypher_functions.url') ),
    path("mem", views.mem, name="mem"),   
    path("logout", views.logout_view, name="logout"),
    path('upload_fingerprint/', views.upload_fingerprint, name='upload_fingerprint'),
]
