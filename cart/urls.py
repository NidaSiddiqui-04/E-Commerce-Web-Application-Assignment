from django.urls import path
from . import views
app_name='cart'
urlpatterns = [
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('', views.view_cart, name='view_cart'),
    path('remove/<int:product_id>',views.remove_from_cart,name='remove'),
    path('remove_item/<int:product_id>',views.decrease_cart_item,name='removeitem'),
    path('checkout/<int:cart_id>',views.checkout,name='checkout'),
    path("order_placed",views.order_placed,name="order_placed"),
    path('order_history/',views.order_history,name='order_history'),
    path('cancel/<int:id>/',views.cancel_order,name='cancel_order'),
    path('cancel_confirmation/<int:id>/',views.cancel_confirmation,name='cancel_confirmation')
]