from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/confirm/', views.order_confirm, name='order_confirm'),
    path('paypal/pay/<int:order_id>/', views.paypal_payment, name='paypal_payment'),
    path('paypal/success/<int:order_id>/', views.paypal_success, name='paypal_success'),
    path('paypal/cancel/<int:order_id>/', views.paypal_cancel, name='paypal_cancel'),
    path('advisor/', views.shopping_advisor, name='shopping_advisor'),
]