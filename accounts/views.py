from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import PendingRegistration
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
import random
from django.contrib.auth.decorators import login_required
# Create your views here.
#Register View------------------------------------------------------------
def _generate_otp():
    return str(random.randint(10000,99999))

def register_view(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method=="POST":
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()

        if not full_name or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return render(request, "accounts/register.html", {"full_name": full_name, "email": email})
        
        if password1!=password2:
            messages.error(request, "Password do not match.")
            return render(request,'accounts/register.html')
        
        username = email.split('@')[0]
        if User.objects.filter(username=username).exists():
            username = f"{username}{random.randint(100,999)}"
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request,'accounts/register.html')
        
        otp = _generate_otp()
        password_hash = make_password(password1)

        pending, _ = PendingRegistration.objects.update_or_create(
            email = email,
            defaults = {
                "username":username,
                "full_name":full_name,
                "password_hash": password_hash,
                "otp_code":otp,
            },
        )

        send_mail(
            subject="CampusCart Verification Code",
            message=f"Your verification code is: {otp}\nThis code expires in 10 minutes.",
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )

        request.session["pending_email"] = email
        messages.success(request,"Verification code sent to your email.")

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
        
        if hasattr(pending, 'full_name') and pending.full_name:
            name_parts = pending.full_name.split(' ', 1)
            user.first_name = name_parts[0]
            user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            user.save()

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



#Login View --------------------------------------------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None
        
        if user is None:
            messages.error(request, "Invalid email or password.")
            return render(request, 'accounts/login.html', {'email': email})
        
        login(request, user)
        return redirect('home')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


from .models import Profile
from products.models import Product
@login_required

def user_profile_view(request):
    # Get or create profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Handle form submission - HTML form
    if request.method == 'POST':
        # Update user full name
        full_name = request.POST.get('full_name', '').strip()
        if full_name:
            name_parts = full_name.split(' ', 1)
            request.user.first_name = name_parts[0]
            request.user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            request.user.save()
        
        # Update profile with form data
        profile.bio = request.POST.get('bio', '')
        profile.phone = request.POST.get('phone', '')
        profile.department = request.POST.get('department', '')
        profile.batch = request.POST.get('batch', '')  
        
        # Handle profile photo upload
        if 'profile_photo' in request.FILES:
            profile.profile_photo = request.FILES['profile_photo']
        
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    # Product statistics
    total = Product.objects.filter(seller=request.user).count()
    available = Product.objects.filter(seller=request.user, is_available=True).count()
    sold = Product.objects.filter(seller=request.user, is_available=False).count()
    
    context = {
        "profile": profile,
        "total": total,
        "available": available,
        "sold": sold,
        "created": created,
    }
    
    return render(request, "accounts/profile.html", context)







