"""
URL configuration for sandbox_testing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from django.urls import path, include
from pcdprocessor.views import  sandbox
from pcdprocessor.views import index
from pcdprocessor.views import compile_code
from pcdprocessor.views import upload_points
urlpatterns = [
    path('admin/', admin.site.urls),
    path('pcdprocessor/', include('pcdprocessor.urls')),
    path('api/sandbox/', sandbox),
    path('', index, name='index'),
    path('compile/', compile_code, name='compile'),
    path('upload_points/',upload_points, name='upload_points'),
]

