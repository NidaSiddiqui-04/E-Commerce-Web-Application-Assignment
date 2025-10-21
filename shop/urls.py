from . import views
from django.urls import path

app_name='shop'
urlpatterns=[
    path('',views.dashboard,name='dashboard'),
    path('detail_view/<int:pk>/',views.detail_view_page,name='detail_view')
]