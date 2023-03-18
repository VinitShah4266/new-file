from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from uuid import uuid4
from passlib.hash import pbkdf2_sha256
from customer.views import index as cust_home
from sqlalchemy import desc


# Create your views here.


def seller_index(request):
    seller = Seller.objects.get(email = request.session["email"])
    product = Product.objects.filter(trader=seller)
    context = {
        "seller" : seller,
        "product" : product
    }
    return render(request, "seller-index.html", context=context)


def seller_email_register(request):
    if request.method == "POST":
        print("\n\n\nstage 1\n\n\n")
        try: 
            print("\n\n\nstage 2\n\n\n")
            seller = Seller.objects.get(email = request.POST["email"])
            print("\n\n\nstage 3\n\n\n")
            context - {
                "msg_d" : "Email already Registered",
                "email_id" : seller.email,
            }
            print("\n\n\nstage 4\n\n\n")
            return render(request, "seller-email-register.html", context=context)
        except:
            print("\n\n\nstage 5\n\n\n")
            otp = str(uuid4())[:6]
            email = request.POST["email"]
            verify_seller = Seller_Authenticate.objects.create(
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
            return render(request, "seller-otp.html", context=context)
    else:
        print("\n\n\nstage 8\n\n\n")
        return render(request, "seller-email-register.html")


def seller_otp(request):
    if request.method == "POST":
        email = request.POST["email"]
        print(f"\n\n\nstage 1\n\n\n")
        try:
            print(f"\n\n\nstage 2\n\n\n")
            auth_code = Seller_Authenticate.objects.get(email=email)
            if auth_code.auth_otp != request.POST["otp"]:
                context = {
                    "msg_d" : "Invaild OTP",
                    "email" : email
                }
                return render(request, "seller-otp.html", context=context)
            else:
                try:
                    Seller_Authenticate.objects.get(email = email, auth_otp=request.POST["otp"])
                    context = {
                        "email_id" : email,
                    }
                    return render(request, "seller-signup.html", context=context)
                except Exception as e:
                    print(f"\n\n\n{e}\n\n\n")
                    return render(request, "seller-otp.html", context=context)
        except Exception as e:
            print(f"\n\n\nstage 3\n\n\n")
            print(f"\n\n\n{e}\n\n\n")
            context = {
                "msg_d" : "Something went Worng...",
                "email" : email
            }
            return render(request, "seller-otp.html", context=context)
    else:
        return render(request, "seller-otp.html")


def seller_signin(request):
    if request.method == "POST":
    
        # if email and password is empty then show msg

        if request.POST["email"] == "" or request.POST["password"] == "":
            context = {
            "msg_d" : "Please enter Email and Password to sign in...",
           }
            return render(request, "seller-signin.html", context=context)
        else:

            # store email

            email_id = request.POST["email"]
            rawPassword = request.POST["password"]

            # if email and password is match then create a session and load to home page

            try:
                user = Seller.objects.get(email=email_id)
                flag = user.verify_password(rawPassword)
                if flag:
                # create a session of email for sign in
                    request.session["email"] = user.email
                    return redirect("seller_home")
                else:
                    context = {
                        "msg_d" : "Incorrect Password"
                    }
                    return render(request, "seller-signin.html", context=context)
            except Exception as e:
                print(f"\n\n\n{e}\n\n\n")
                try:

                    # if password doesn't matches then show msg

                    user = Seller.objects.get(email=request.POST["email"])
                    context = {
                        "msg_d" : "Incorrect Password...",
                        "email_id" : email_id
                    }
                    return render(request, "seller-signin.html", context=context)

                    # if email and password both not matches then show msg

                except:
                    context = {
                        "msg_d" : "Look like you are not registered with us yet",
                        "email_id" : email_id
                    }
                    return render(request, "seller-signin.html", context=context)
    else:
        return render(request, "seller-signin.html")


def seller_signup(request):
    if request.method == "POST":
        email = request.POST["email"]
        try:

            # checking all the values are fill if not then show msg_d
            print(f"\n\n\nstage 1\n\n\n")
            auth_user = Seller_Authenticate.objects.get(email = email)
            if request.POST["fname"] == "" or request.POST["lname"] == "" or request.POST["email"] == "" or request.POST["phone"] == "" or request.POST["address"] == "" or request.POST["password"] == "" or request.POST["c_password"] == "":
                
                context = {
                    "msg_d" : "All Fields are Mandatory...",
                    "email_id" : email
                }
                return render(request, "seller-signup.html", context=context)


            # if passwd and con_passwd is same then it will create account.

            elif request.POST["password"] == request.POST["c_password"]:
                print(f"\n\n\nstage 2\n\n\n")

                userEnteredPassword = request.POST["password"]

                encyPassword = pbkdf2_sha256.hash(userEnteredPassword)

                # creating user object to store in db

                print(f"\n\n\nstage 3\n\n\n")
                seller = Seller.objects.create(
                fname = request.POST["fname"],
                lname = request.POST["lname"],
                email = auth_user.email,             
                phone = request.POST["phone"],
                address = request.POST["address"],
                password = encyPassword,
                )
                seller.save()

                print(f"\n\n\nstage 3\n\n\n")
                auth_user.is_verify = True
                auth_user.save()

                auth_user.delete()

                print(f"\n\n\nstage 4\n\n\n")
                subject = f"Account Created Successfully"
                message = f"Hello {seller.fname} your account has been created successfully in coza-store\nThank You for choosing our services"
                email_from =  settings.EMAIL_HOST_USER
                recipient_list = [email,]
                send_mail(subject, message, email_from, recipient_list)
                context = {
                    "msg_s" :  "Account Created Successfully...",
                    "email_id" : seller.email
                }
                return render(request, "seller-signin.html", context=context)

            # if passwd and con_passwd Don't match

            else:
                context = {
                    "email_id" : email,
                    "msg_d" :  "Password and Conform password does not match"
                }
                return render(request, "seller-signup.html", context=context)
        except  Exception as e:
            print(f"\n\n\n{e}\n\n\n")
            context = {
                    "email_id" : email,
                    "msg_d" :  "Something went wrong..."
                }
            return render(request, "seller-signup.html", context=context)
    else:
        context = {
            "email_id" : email,
        }
        return render(request, "seller-signup.html", context=context)


def seller_signout(request):
    try:

        # Delete the session to sign out

        del request.session["email"]
        request.session.flush()
        return redirect(cust_home)
    except Exception as e :
        context = {
            "msg_d" : "Signout was unsuccessful, please contact to us...",
        }
        return render(request, "seller-index.html", context=context)


def add_product(request):
    try:
        seller = Seller.objects.get(email = request.session["email"])
        if request.method == "POST":
            if request.POST["title"] == "" or request.POST["price"] == "" or request.POST["trader"] == "" or request.POST["quantity"] == "" or request.POST["desc"] == "":
                context ={
                    "msg_d" : "All Fields are mandatory, but IN Stock"
                }
                return render(request, "seller-addproduct.html", context=context)
            else:
                product = Product.objects.create(
                    title = request.POST["title"],
                    price = request.POST["price"],
                    quantity = request.POST["quantity"],
                    trader = seller,
                    desc = request.POST["desc"],
                )
                if "image" in request.FILES:
                    product.image = request.FILES["image"]
                    product.save()
                    context ={
                        "msg_s" : "Product Uploaded with Image"
                    }
                    return render(request, "seller-addproduct.html", context=context)
                else:
                    context ={
                        "msg_s" : "Product Uploaded without Image"
                    }
                    return render(request, "seller-addproduct.html", context=context)
        else:
            return render(request, "seller-addproduct.html")
    except Exception as e :
        print(f"\n\n\n{e}\n\n\n")
        return redirect("seller_signin")


def edit_product(request, pk):
    seller = Seller.objects.get(email = request.session["email"])
    product = Product.objects.get(pk=pk, trader=seller)

    if request.method == "POST":
        if request.POST["title"] == "" or request.POST["price"] == "" or request.POST["quantity"] == "":
            context = {
                "msg_d" : "All Fields are Mandatory ",
                "product" : product,
                "seller" : seller
            }
            return render(request, 'seller-editproduct.html', context=context)
        else:
            product.title = request.POST["title"]
            product.price = request.POST["price"]
            product.quantity = request.POST["quantity"]

            product.save()

            if request.POST["desc"] == "":
                product.desc = ""
                product.save()
            else:
                product.desc = request.POST["desc"]
                product.save()

            if "image" in request.FILES:
                product.image = request.FILES["image"]
                product.save()
                context = {
                    "msg_s" : "Product updated Successfully with image",
                    "product" : product,
                    "seller" : seller
                }
                return render(request, 'seller-editproduct.html', context = context)
            else:
                context = {
                    "msg_s" : "Product updated Successfully without image",
                    "product" : product,
                    "seller" : seller
                }
                return render(request, 'seller-editproduct.html', context = context)
    else:
        context = {
            "product" : product,
            "seller" : seller
        }
        return render(request, 'seller-editproduct.html', context = context)

def delete_product(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect("seller_home")