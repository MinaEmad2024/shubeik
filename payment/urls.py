from django.urls import path 
from .import views


urlpatterns = [
    path('payment_success',views.payment_success, name='payment_success'),
    path('checkout/<str:category>',views.checkout, name='checkout'),
    path('billing_info/<str:category>', views.billing_info, name='billing_info'),
    path('process_order/<str:category>', views.process_order, name='process_order'),
    path('shipped_dash', views.shipped_dash, name='shipped_dash'),
    path('not_shipped_dash', views.not_shipped_dash, name='not_shipped_dash'),
    path('orders/<int:pk>', views.orders, name='orders'),
    path('admin_dash', views.admin_dash, name='admin_dash'),
    path('admin_orders_dash/<int:id>', views.admin_orders_dash, name='admin_orders_dash'),
]