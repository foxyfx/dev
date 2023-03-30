from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings
import os
from .models import MyUser

def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def home(reqeust):
    return render(reqeust,'home.html', {'navbar' : 'home'})

@authenticated_user
def login_view(request):
    context = {'navbar': 'login'}
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.success(request, "Le mot de passe ou le nom d'utilisateur est incorrect ")
            return redirect('login')
    else:
        return render(request, 'login.html', context)



@authenticated_user
def signup(request):
    if request.method == 'POST':
        # Get the form data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cv_file = request.FILES['cv']
        facebook_username = request.POST['facebook_username']
        facebook_password = request.POST['facebook_password']
        instagram_username = request.POST['instagram_username']
        instagram_password = request.POST['instagram_password']
        checkbox1 = request.POST.get('superviseur', False)
        checkbox2 = request.POST.get('student', False)

        # Create a new user object
        user = MyUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            cv=cv_file,
            facebook_username=facebook_username,
            facebook_password=facebook_password,
            instagram_username=instagram_username,
            instagram_password=instagram_password,
            checkbox1=checkbox1,
            checkbox2=checkbox2,
        )

        # Save additional user data
        user.save()

        # Authenticate the user and redirect to the login page
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('login')
    else:
        context = {'navbar': 'signup'}
        return render(request, 'signup.html', context)


    
@login_required(login_url='login')
def profile(request):
    user = request.user
    # Retrieve the user's information from the database
    try:
        user_info = MyUser.objects.get(email=user.email)
    except MyUser.DoesNotExist:
        user_info = None

    context = {
        'title': f"Profile - {user.email}",
        'navbar': 'profile',
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, 'déconnexion réussie :)')
    return redirect('login')



def check_email(request):
    if request.method == 'GET' and 'email' in request.GET:
        email = request.GET['email']
        if MyUser.objects.filter(email=email).exists():
            return JsonResponse({'exists': True})
        else:
            return JsonResponse({'exists': False})
    else:
        return JsonResponse({'error': 'Invalid request'})


