from django.urls import path
from .views import *

urlpatterns = [
    path("seller-index", seller_index, name="seller_home"),
    path("seller-signin/", seller_signin, name="seller_signin"),
    path("seller-email-register/", seller_email_register, name="seller_email_register"),
    path("seller-otp/", seller_otp, name="seller_otp"),
    path("seller-signup/", seller_signup, name="seller_signup"),
    path("seller-signout/", seller_signout, name="seller_signout"),
    path("add-product/", add_product, name="add_product"),
    path("edit-product/<int:pk>", edit_product, name="edit_product"),
    path("delete-product/<int:pk>", delete_product, name="delete_product"),
]