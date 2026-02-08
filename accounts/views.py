from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
#Register View
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method=="POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()

        if password1!=password2:
            messages.error(request, "Password do not match.")
            return render(request,'accounts/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request,'accounts/register.html')
        
        user = User.objects.create_user(
            username = username,
            email=email,
            password=password1
        )

        login(request,user)
        return redirect('home')
    
    return render(request,'accounts/register.html')


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





