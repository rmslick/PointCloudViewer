from django.urls import path
from .views import index

from . import views

urlpatterns = [
    path('hello/', views.hello),
    path('', index, name='index'),
    path('compile/', views.compile_code, name='compile'),
    path('upload_points/', views.upload_points, name='upload_points'),

]