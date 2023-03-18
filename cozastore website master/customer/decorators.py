from django.shortcuts import render
from .models import *



def customer_check_session(func):
    def inner(request, *args, **context):
        try:
            if 'email' in request.session:
                customer = Customer.objects.get(email=request.session["email"])
                context["customer"] = customer 
                return func(request, *args, **context)
            else:
                return func(request, *args, **context)
        except:
            return func(request, *args, **context)
    return inner