from django.urls import path

from . import views

app_name = "gb"
urlpatterns = [
    path('', views.index, name='index'),
    path('getAuth', views.getAuth, name='getAuth'),
    path('authConfirmed', views.authConfirmed, name='authConfirmed'),
    path('doBackup', views.doBackup, name='doBackup'),
    path('adhocBackup', views.adhocBackup, name='adhocBackup'),
]