from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Contact)
admin.site.register(Customer)
admin.site.register(Authenticate)
admin.site.register(Wishlist)
admin.site.register(Cart)