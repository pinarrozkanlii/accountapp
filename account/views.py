from django.shortcuts import render,redirect
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from authdemo import settings
from django.core.mail import send_mail,EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_text
from .tokens import generate_token

# Create your views here.
def home(request):
    return render(request, "account/index.html")

def signup(request):

    #if request.method=="POST":
    if request.POST.get('method')=='post':
        email=request.POST["email"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]

        if User.objects.filter(email=email):
            messages.error(request,"Email is already exist")
            return redirect('home')

        if password1 != password2:
            messages.error(request,"Passwords did not match")    

        myuser=User.objects.create_user(email,password1)
        myuser.email=email
        myuser.active=False 
        myuser.save() 

        messages.success(request,"Your Account has been succesfully created.We have sent you a confirmation email.\nPlease confirm your email address.")


        subject="Welcome"
        message="welcome our delicious world. \n Please confirm your email address to continue"
        from_email=settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)


        current_site=get_current_site(request)
        email_subject="Confirm your email"
        message2=render_to_string('email_confirmation.html',{
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token':generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            to=[myuser.email],

        )
        email.fail_silently=True
        email.send()

        return redirect('signin')
    return render(request, "account/signup.html")


def signin(request):

    if request.method == "POST":
    
        email= request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email,password=password)

        if user is not None:
            login(request,user)
            email=user.email
        
            return render(request,"account/index.html",{'email':email})
        else:
            messages.error(request,"Bad Credentials")
            return redirect('home')    

    return render(request, "account/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged Out Successfully!")
    return redirect('home')    



def activate(request,uidb64,token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))
        myuser=User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser=None
    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.active=True #active -> is_active
        myuser.save()
        login(request,myuser)
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')    

