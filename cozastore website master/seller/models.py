from distutils.command.upload import upload
from email.policy import default
from tabnanny import verbose
from django.db import models
from passlib.hash import pbkdf2_sha256


# Create your models here.

class Seller(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=90)
    email = models.EmailField(unique=True)
    phone = models.BigIntegerField(unique=True)
    address = models.TextField()
    password = models.CharField(max_length=255)

    def verify_password(self, rawPassword):
        return pbkdf2_sha256.verify(rawPassword, self.password)

    @staticmethod
    def get_seller_by_email(email):
        return Seller.objects.get(email)
    
    def __str__(self):
        return self.fname
    
    class Meta:
        verbose_name = "Seller"
        verbose_name_plural = "Seller"


class Seller_Authenticate(models.Model):
    email = models.EmailField()
    auth_otp = models.CharField(max_length=30)
    is_verify = models.BooleanField(default=False)
    is_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email

class Product(models.Model):
    title = models.CharField(max_length=150)
    price = models.PositiveIntegerField()
    trader = models.ForeignKey(Seller, on_delete =models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    desc = models.TextField()
    image = models.ImageField(upload_to="images/product/", default = "images/sample.jpg")
    in_stock = models.BooleanField(default=False)

    def __str__(self):
        return self.title

