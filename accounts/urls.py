from . import views
from django.urls import path
from django.contrib.auth.views import LoginView
from django import views as a_view

app_name='accounts'

urlpatterns=[
    path('register/',views.register,name='register'),
    path('login/',LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/',views.logout_view,name='logout')
]