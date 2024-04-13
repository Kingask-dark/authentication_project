from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def home(request):
        if not request.user.is_authenticated:
            return redirect('/login/')
        else:
            return render(request, 'authentication_app/html/home.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication_app/html/signup.html', {'form': form})

# def user_login(request):
#     if request.method == 'POST':
#         form = CustomAuthenticationForm(request, request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, email=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#     else:
#         form = CustomAuthenticationForm()
#     return render(request, 'authentication_app/html/login.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data['username'] 
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'authentication_app/html/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')