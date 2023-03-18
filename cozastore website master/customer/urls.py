from django.urls import path
from .views import *

urlpatterns = [                          
    path("",index, name = "home"),
    path("contact/",contact, name = "contact"),
    path("customer_email_register/",customer_email_register, name = "customer_email_register"),
    path("customer_otp/",customer_otp, name = "customer_otp"),
    path("signup/",signup, name = "signup"),
    path("signin/",signin, name = "signin"),
    path("signout/",signout, name = "signout"),
    path("profile/",profile, name = "profile"),
    path("change_password/",change_password, name = "change_password"),
    path("add-to-wishlist/<int:pk>",add_to_wishlist, name = "add_to_wishlist"),
    path("wishlist-cart/",wishlist_cart, name = "wishlist_cart"),
    path("delete-wishlist-item/<int:pk>/", delete_wishlist_item, name="delete_wishlist_item"),
    path("clear-wishlist/", clear_wishlist, name="clear_wishlist"),
    path("product-cart/",product_cart_display, name = "product_cart_display"),
    path("cart-product/<int:pk>/",add_to_cart, name = "add_to_cart"),
    path("aboutus/",About_Us, name = "About US"),
]