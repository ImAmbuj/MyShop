from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.index , name="index"),
    path('Accounts', views.accounts , name="accounts"),
    path('Products', views.products , name="products"),
    path('AboutUs', views.about , name="about"),
    path('ContactUs', views.contact , name="contact"),
    path('Cart', views.cart , name="cart"),
    path('Logout', views.logout , name="logout"),
    path('Checkout', views.checkout , name="checkout"),
    path('handlerequest', views.handlerequest , name="handlerequest"),
    path('Product/<slug:product_slug>', views.product , name="product"),
    path('Add-to-cart/<slug:product_slug>', views.add_to_cart , name="add_to_cart"),
    path('Remove-from-cart/<slug:product_slug>', views.remove_from_cart , name="remove_from_cart"),
    path('Decrease-quantity/<slug:product_slug>', views.decrease_quantity , name="decrease_quantity")
    
]