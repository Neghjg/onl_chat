from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from chat.models import ChatMessage3
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


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('authorization:profile'))
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'authorization/profile.html', {"form": form,
                                                          'title': 'Профиль'})
    
    
def index_redirect(request):
    if not request.user.is_authenticated:
        return redirect("authorization:registration", permanent=True)
    elif request.user.is_authenticated:
        chats = ChatMessage3.objects.filter(user=request.user).order_by("-updated")
        room_id = chats[0].id
        return redirect("chat:room", room_id=room_id, permanent=True)
    