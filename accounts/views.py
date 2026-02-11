from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import PendingRegistration
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
import random
# Create your views here.
#Register View--------------------------------------
def _generate_otp():
    return str(random.randint(10000,99999))

def register_view(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method=="POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()

        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return render(request, "accounts/register.html", {"username": username, "email": email})
        
        if password1!=password2:
            messages.error(request, "Password do not match.")
            return render(request,'accounts/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request,'accounts/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request,'accounts/register.html')
        
        otp = _generate_otp()
        password_hash = make_password(password1)

        pending, _ = PendingRegistration.objects.update_or_create(
            email = email,
            defaults = {
                "username":username,
                "password_hash": password_hash,
                "otp_code":otp,
            },
        )

        # user = User.objects.create_user(
        #     username = username,
        #     email=email,
        #     password=password1
        # )

        # send otp email
        send_mail(
            subject="CampusCart Lite Verification Code",
            message=f"Your verification code is: {otp}\nThis code expires in 10 minutes.",
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )

        request.session["pending_email"] = email
        messages.success(request,"Verification code sent to your email.")

        # login(request,user)
        return redirect('verify_email')
    
    return render(request,'accounts/register.html')

def verify_email_view(request):
    email = request.session.get("pending_email")

    if not email:
        messages.error(request, "No pending verification found. Please register again.")
        return redirect("register")
    
    pending = PendingRegistration.objects.filter(email = email).first()
    if not pending:
        messages.error(request,"No pending verification found. Please register again.")
        return redirect("register")
    
    if request.method == "POST":
        code = request.POST.get("code", "").strip()

        if pending.is_expired():
            messages.error(request, "Code expired. Please resend code.")
            return redirect("verify_email")
        if code != pending.otp_code:
            messages.error(request, "Invalid verification code.")
            return render(request, "accounts/verify_email.html", {"email": email})
        
        user = User.objects.create(
            username = pending.username,
            email=pending.email,
            password = pending.password_hash,
        )

        pending.delete()
        request.session.pop("pending_email", None)

        login(request,user, backend="django.contrib.auth.backends.ModelBackend")
        messages.success(request, "Email verified! Account created successfully.")
        return redirect("home")
    
    return render(request, "accounts/verify_email.html", {"email": email})


def resend_code_view(request):
    email = request.session.get("pending_email")
    if not email:
        messages.error(request, "No pending verification found.")
        return redirect("register")

    pending = PendingRegistration.objects.filter(email=email).first()
    if not pending:
        messages.error(request, "No pending verification found.")
        return redirect("register")

    otp = _generate_otp()
    pending.otp_code = otp
    pending.save()

    send_mail(
        subject="CampusCart Lite Verification Code (Resend)",
        message=f"Your new verification code is: {otp}\nThis code expires in 10 minutes.",
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )

    messages.success(request, "A new verification code has been sent.")
    return redirect("verify_email")



#Login View ---------------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request,username = username, password = password)
        if user is None:
            messages.error(request,"Invalid username or password.")
            return render(request,'accounts/login.html', {'username':username})
        
        else:
            login(request,user)
            return redirect('home')
        

    return render(request,'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')





