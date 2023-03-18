from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from .decorators import customer_check_session
from uuid import uuid4
from passlib.hash import pbkdf2_sha256
from seller.models import *


# Create your views here

@customer_check_session
def index(request, *args, **context):
    product = Product.objects.all()
    wishlist = Wishlist.objects.all()
    context.update({
        "product" : product,
        "wishlist" : wishlist
    })
    return render(request, "index.html",context=context)


@customer_check_session
def contact(request, *args, **context):
    try:
        if request.method == "POST":
            try:
                if request.POST["fname"] == "" or request.POST["lname"] == "" or request.POST["email"] == "" or request.POST["subject"] == "" or request.POST["message"] == "":
                    context = {
                        "msg_d" : "All fields are mandatory..."
                    }
                    return render(request, "contact.html", context=context)
                # creating user object to store in db
                else:
                    user = Contact.objects.create(
                    fname = request.POST["fname"],
                    lname = request.POST["lname"],
                    subject = request.POST["subject"],
                    email = request.POST["email"],             
                    message = request.POST["message"]
                    )
                    user.save()

                #    Email for host

                    subject = f"Message received from {user.email}"
                    message = f"Subject : {user.subject} \nMessage : {user.message}"
                    email_from =  settings.EMAIL_HOST_USER
                    recipient_list = [settings.EMAIL_HOST_USER,]
                    send_mail(subject, message, email_from, recipient_list)
                

                #    Email for user

                    subject = f"Contact request sent Successfully"
                    message = f"Hello {user.fname},\nYour message has been recevied by our team. we will contact you in a short time.\n\nWell Regrad from Coza-store team.\nThank You."
                    email_from =  settings.EMAIL_HOST_USER
                    recipient_list = [user.email,]
                    send_mail(subject, message, email_from, recipient_list)

                    
                    context.update({
                        "msg_s" : "Message sent Successfully"
                    })

                    return render(request, "contact.html", context=context)
            except Exception as e:
                print(f"\n\n\n{e}n\n\n")
                context.update({
                    "msg_d" : "Something went wrong..."
                    })
                return render(request, "contact.html", context=context)
        else:
            return render(request, "contact.html", context=context)
    except Exception as e:
        print(f"\n\n\n{e}\n\n\n")
        context = {
            "msg_d" : "Something went wrong..."
            }
        return render(request, "contact.html", context=context)


def customer_email_register(request):
    if request.method == "POST":
        print("\n\n\nstage 1\n\n\n")
        try: 
            print("\n\n\nstage 2\n\n\n")
            customer = Customer.objects.get(email = request.POST["email"])
            print("\n\n\nstage 3\n\n\n")
            context - {
                "msg_d" : "Email already Registered",
                "email_id" : customer.email,
            }
            print("\n\n\nstage 4\n\n\n")
            return render(request, "customer_email_register.html", context=context)
        except:
            print("\n\n\nstage 5\n\n\n")
            otp = str(uuid4())[:6]
            email = request.POST["email"]
            verify_customer = Authenticate.objects.create(
                email = email,
                auth_otp = otp 
            )
            print("\n\n\nstage 6\n\n\n")
            subject = f"Email Registeration OTP | Do not Reply"
            message = f"Your Email Registeration OTP is {otp}"
            email_from =  settings.EMAIL_HOST_USER
            recipient_list = [email,]
            send_mail(subject, message, email_from, recipient_list)
            print("\n\n\nstage 7\n\n\n")
            context = {
                "email" : email
            }
            return render(request, "customer_otp.html", context=context)
    else:
        print("\n\n\nstage 8\n\n\n")
        return render(request, "customer_email_register.html")


def customer_otp(request):
    if request.method == "POST":
        email = request.POST["email"]
        print(f"\n\n\nstage 1\n\n\n")
        try:
            print(f"\n\n\nstage 2\n\n\n")
            auth_code = Authenticate.objects.get(email=email)
            if auth_code.auth_otp != request.POST["otp"]:
                context = {
                    "msg_d" : "Invaild OTP",
                    "email" : email
                }
                return render(request, "customer_otp.html", context=context)
            else:
                try:
                    Authenticate.objects.get(email = email, auth_otp=request.POST["otp"])
                    context = {
                        "email_id" : email,
                    }
                    return render(request, "signup.html", context=context)
                except Exception as e:
                    print(f"\n\n\n{e}\n\n\n")
                    return render(request, "customer_otp.html", context=context)
        except Exception as e:
            print(f"\n\n\nstage 3\n\n\n")
            print(f"\n\n\n{e}\n\n\n")
            context = {
                "msg_d" : "Something went Worng...",
                "email" : email
            }
            return render(request, "customer_otp.html", context=context)
    else:
        return render(request, "customer_otp.html", context=context)


def signup(request):
    email = request.POST["email"]
    if request.method == "POST":
        try:

            # checking all the values are fill if not then show msg_d
            print(f"\n\n\nstage 1\n\n\n")
            auth_user = Authenticate.objects.get(email = email)
            if request.POST["fname"] == "" or request.POST["lname"] == "" or request.POST["email"] == "" or request.POST["phone"] == "" or request.POST["address"] == "" or request.POST["password"] == "" or request.POST["c_password"] == "":
                
                context = {
                    "msg_d" : "All Fields are Mandatory...",
                    "email_id" : email
                }
                return render(request, "signup.html", context=context)


            # if passwd and con_passwd is same then it will create account.

            elif request.POST["password"] == request.POST["c_password"]:
                print(f"\n\n\nstage 2\n\n\n")

                userEnteredPassword = request.POST["password"]

                encyPassword = pbkdf2_sha256.hash(userEnteredPassword)

                # creating user object to store in db

                print(f"\n\n\nstage 3\n\n\n")
                customer = Customer.objects.create(
                fname = request.POST["fname"],
                lname = request.POST["lname"],
                email = auth_user.email,             
                phone = request.POST["phone"],
                address = request.POST["address"],
                password = encyPassword,
                )
                customer.save()

                print(f"\n\n\nstage 3\n\n\n")
                auth_user.is_verify = True
                auth_user.save()

                auth_user.delete()

                print(f"\n\n\nstage 4\n\n\n")
                subject = f"Account Created Successfully"
                message = f"Hello {customer.fname} your account has been created successfully in coza-store\nThank You for choosing our services"
                email_from =  settings.EMAIL_HOST_USER
                recipient_list = [email,]
                send_mail(subject, message, email_from, recipient_list)
                context = {
                    "msg_s" :  "Account Created Successfully...",
                    "email_id" : customer.email
                }
                return render(request, "signin.html", context=context)

            # if passwd and con_passwd Don't match

            else:
                context = {
                    "email_id" : email,
                    "msg_d" :  "Password and Conform password does not match"
                }
                return render(request, "signup.html", context=context)
        except  Exception as e:
            print(f"\n\n\n{e}\n\n\n")
            context = {
                    "email_id" : email,
                    "msg_d" :  "Something went wrong..."
                }
            return render(request, "signup.html", context=context)
    else:
        context = {
            "email_id" : email,
        }
        return render(request, "signup.html", context=context)


def signin(request):
    if request.method == "POST":

        # if email and password is empty then show msg

        if request.POST["email"] == "" or request.POST["password"] == "":
            context = {
            "msg_d" : "Please enter Email and Password to sign in...",
           }
            return render(request, "signin.html", context=context)
        else:

            # store email

            email_id = request.POST["email"]
            rawPassword = request.POST["password"]

            # if email and password is match then create a session and load to home page

            try:
                user = Customer.objects.get(email=email_id)
                flag = user.verify_password(rawPassword)
                if flag:
                # create a session of email for sign in
                    request.session["email"] = user.email
                    return redirect("home")
                else:
                    context = {
                        "msg_d" : "Incorrect Password"
                    }
                    return render(request, "signin.html", context=context)
            except Exception as e:
                print(f"\n\n\n{e}\n\n\n")
                try:

                    # if password doesn't matches then show msg

                    user = Customer.objects.get(email=request.POST["email"])
                    context = {
                        "msg_d" : "Incorrect Password...",
                        "email_id" : email_id
                    }
                    return render(request, "signin.html", context=context)

                    # if email and password both not matches then show msg

                except:
                    context = {
                        "msg_d" : "Look like you are not registered with us yet",
                        "email_id" : email_id
                    }
                    return render(request, "customer_email_register.html", context=context)
    else:
        return render(request, "signin.html")


def signout(request):
    try:

        # Delete the session to sign out

        del request.session["email"]
        return redirect("home")
    except Exception as e :
        context = {
            "msg_d" : "Signout was unsuccessful, please contact to us...",
        }
        return render(request, "contact.html", context=context)


@customer_check_session
def profile(request, *args, **context):
    try:

        # fetch the email of user from db if there is session is already created
        # customer = Customer.objects.get(email = request.session["email"])

        if request.method == "POST":
            
                # Check weather fname and lname is empty and show msg

                if request.POST["fname"] == "" or request.POST["lname"] == ""  or request.POST["address"] == "":  

                    context.update({
                        "msg_d" : "First Name, Last Name and Address are Mandatory...",
                        "customer" : customer,
                    })
                    return render(request, "profile.html", context=context)
                else:
                    try:
                    # update the profile and show msg
                    
                        context["customer"].fname = request.POST["fname"]
                        context["customer"].lname = request.POST["lname"]
                        context["customer"].address = request.POST["address"]
                        context["customer"].save()

                        context.update({
                            "msg_s" : "Your Profile Has been Updated Successfully...",
                            "customer" : customer,
                        })
                        return render(request, "profile.html", context=context)
                    except Exception as e:
                        print(f"\n\n\n{e}\n\n\n")
                        context.update({
                            "msg_d" : "Something went wrong...",
                            "customer" : customer
                        } )
                        return render(request, "profile.html", context=context)
        else:
            return render(request, "profile.html", context=context)
    except Exception as e:
        print(f"\n\n\n{e}\n\n\n")
        context.update({
            "msg_d" : "Seems that you are not login please login...",
                "customer" : customer
        })
        return render(request, "signin.html", context=context)


@customer_check_session
def change_password(request, *args, **context):
    try: 
        if request.method == "POST":
            if request.POST["o_password"] == "" or request.POST["password"] == "" or request.POST["c_password"] == "":
                context.update ({
                    "pmsg_d" : "All fields are mandatory",
                            })
                return render(request, "profile.html", context=context)
            elif request.POST["o_password"] == context["customer"].password:
                    if request.POST["password"] != request.POST["o_password"]:
                        if request.POST["password"] == request.POST["c_password"]:
                                try:

                                    userEnteredPassword = request.POST["password"]
                                    encyPassword = pbkdf2_sha256.hash(userEnteredPassword)

                                    context["customer"].password = encyPassword
                                    context["customer"].save()

                                    context.update ({
                                        "pmsg_s" : "Your Password Has Been Changed Successfully",
                                            })
                                    return render(request, "profile.html", context=context)   
                                except Exception as e:
                                    print(f"\n\n\n{e}\n\n\n")
                                    context.update ({
                                    "pmsg_d" : "Something went Wrong...",
                                                })
                                    return render(request, "profile.html", context=context)
                        else:
                            context.update ({
                                "pmsg_d" : "New Password and Confirm Password doesn't Match...",
                                    })
                            return render(request, "profile.html", context=context)
                    else:
                        context.update ({
                            "pmsg_d" : "New Password and Old Password is Same...",
                                })
                        return render(request, "profile.html", context=context)
            else:
                context.update ({
                    "pmsg_d" : "Old Password is Wrong...",
                        })
                return render(request, "profile.html", context=context)
    except Exception as e:
        context.update ({
        "pmsg_d" : "Something went Wrong...",
        })
        print(f"'\n\n\n{e}\n\n\n")
        return render(request, "profile.html", context=context)
    


####################  WISHLIST  ####################

def add_to_wishlist(request, pk):
    print("\n\n\nStage 1\n\n\n")
    product = Product.objects.get(pk=pk)
    customer = Customer.objects.get(email = request.session["email"])
    try:
        print("\n\n\nStage 2\n\n\n")
        wishlist = Wishlist.objects.get(product=product, customer= customer)
        product = Product.objects.all()
        print("\n\n\nStage 3\n\n\n")
        context = {
            "msg_d" : "Item Already in Wishlist",
            "product" : product,
            "customer" : customer,
            "wishlist" : wishlist 

        }
        print("\n\n\nStage 4\n\n\n")
        return render(request, "index.html", context=context)
    except Exception as e:
        print("\n\n\nStage 5\n\n\n")
        Wishlist.objects.create(customer=customer, product=product)
        product = Product.objects.all()
        print("\n\n\nStage 6\n\n\n")
        context = {
            "msg_s" : "Item Added in Wishlist",
            "product" : product,
            "customer" : customer,
        }
        print("\n\n\nStage 7\n\n\n")
        return render(request, "index.html", context=context)

def wishlist_cart(request):
    customer = Customer.objects.get(email=request.session["email"])
    wishlist = Wishlist.objects.filter(customer=customer)
    print(f"\n\n\n{wishlist}\n\n\n")
    context = {
        "wishlist" : wishlist,
        "customer" : customer
    }
    return render(request, "wishlist-cart.html", context = context)

def delete_wishlist_item(request, pk):
    customer = Customer.objects.get(email=request.session["email"])
    product = Product.objects.get(pk=pk)
    item = Wishlist.objects.get(customer=customer, product = product)
    item.delete()
    return redirect("wishlist_cart")

def clear_wishlist(request):
    customer = Customer.objects.get(email = request.session["email"])
    items = Wishlist.objects.filter(customer=customer)
    items.delete()
    return redirect("wishlist_cart")


####################  CART  ####################

def add_to_cart(request, pk):
    product = Product.objects.get(pk=pk)
    customer = Customer.objects.get(email=request.session["email"])
    try:
        product_in_cart = Cart.objects.get(customer=customer, product=product)
        product_in_cart.product_quantity += 1 
        product_in_cart.total_price = product_in_cart.product_price * product_in_cart.product_quantity
        product_in_cart.save()
        product = Product.objects.all()
        context = {
            "msg_s" : "You have this item in your cart already so we increased the quantity by 1",
            "product" : product,
            "customer" : customer
        }
    except : 
        Cart.objects.create(
            customer = customer,
            product = product,
            product_price = product.price,
            total_price = product.price
        )
        product = Product.objects.all()
        context = {
            "msg_s" : "Item Added to Cart",
            "product" : product,
            "customer" : customer
        }
    return render(request, "index.html", context)
        

def product_cart_display(request):
    net_price = 0
    customer = Customer.objects.get(email=request.session["email"])
    cart = Cart.objects.filter(customer=customer)
    for i in cart:
        net_price += i.total_price
    context = {
        "cart" : cart,
        "customer" : customer,
        "net_price" : net_price,
    }
    return render(request, "shoping-cart.html", context)

def clear_cart(request):
    customer = Customer.objects.get(email = request.session["email"])
    items = Cart.objects.filter(customer=customer)
    items.delete()
    return redirect("shoping-cart")

def About_Us(request):
    return redirect("About_Us")