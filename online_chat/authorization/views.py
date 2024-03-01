from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user, logout
# Create your views here.

def registration(request):
    if request.method == 'POST':
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login_user(request, user)
            #messages.success(request, f'{username}, Вы успешно зарегестрированны и вошли в аккаунт')
            return redirect('/')
    else:
        form = RegistrationUserForm()
    return render(request, 'authorization/registration.html', {'form': form,
                                                               'title': 'Регистрация'})
    
    
def login(request):
    if request.method == 'POST':
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login_user(request, user)
                #messages.success(request, f'{username}, Вы успешно вошли в аккаунт')
                return redirect('/')
    else:
        form = LoginUserForm()
    return render(request, 'authorization/login.html', {'form': form,
                                                        'title': 'Авторизация'})
    
    
def logout_user(request):
    #messages.success(request, f'{request.user.username}, Вы вышли из аккаунта')
    logout(request)
    return redirect("authorization:login")
