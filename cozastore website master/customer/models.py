from django.db import models
from passlib.hash import pbkdf2_sha256
from seller.models import *


# Create your models here.


class Contact(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=90)
    subject = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.fname +  " | "  + self.email


class Customer(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=90)
    email = models.EmailField(unique=True)
    phone = models.BigIntegerField(unique=True)
    address = models.TextField()
    password = models.CharField(max_length=255)

    def verify_password(self, rawPassword):
        return pbkdf2_sha256.verify(rawPassword, self.password)

    @staticmethod
    def get_customer_by_email(email):
        return Customer.objects.get(email)
    
    def __str__(self):
        return self.fname +  " | "  + self.email

class Authenticate(models.Model):
    email = models.EmailField()
    auth_otp = models.CharField(max_length=30)
    is_verify = models.BooleanField(default=False)
    is_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email
    

class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title + " | " + self.customer.fname
    
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_price = models.PositiveIntegerField()
    product_quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField()
    is_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product.title + " | "  + self.customer.fname
    
