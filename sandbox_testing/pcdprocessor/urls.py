from django.urls import path
from .views import index
from .views import rob
from . import views

urlpatterns = [
    path('hello/', views.hello),
    path('', index, name='index'),
    path('rob/', rob, name='rob'),
    path('compile/', views.compile_code, name='compile'),
    path('upload_points/', views.upload_points, name='upload_points'),

]