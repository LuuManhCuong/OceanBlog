"""Ocean URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path("", include('OceanApp.urls')),
    path('admin/', admin.site.urls),
    path('res', include('OceanApp.urls')),
    path('home/', include('OceanApp.urls')),
    path('login', include('OceanApp.urls')),
    path('logout', include('OceanApp.urls')),
    path('check/user', include('OceanApp.urls')),
    path('register', include('OceanApp.urls')),
    path('blog/', include('OceanApp.urls')),
    path('me/blog/', include('OceanApp.urls')),
    path('create/blog/', include('OceanApp.urls')),
    path('delete/blog/', include('OceanApp.urls')),
    path('contact/', include('OceanApp.urls')),
    path('latest/blog', include('OceanApp.urls')),
    path('create/comment', include('OceanApp.urls')),
    path('blog/search', include('OceanApp.urls')),
    path('profile', include('OceanApp.urls')),



]
