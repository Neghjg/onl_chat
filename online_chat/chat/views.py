from django.shortcuts import render, redirect
from authorization.models import User
from chat.models import ChatMessage3
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils import timezone
from .forms import *
from django.contrib import messages



# Create your views here.
def index(request):
    return render(request, "chat/index.html")

def room(request, room_id):
    chats = ChatMessage3.objects.filter(user=request.user).order_by("-updated").prefetch_related("user")
    if room_id == 'None' and chats.exists():
        return render(request, "chat/room.html", {"room_id": chats[0].id, 'user': request.user, "chats": chats})
    elif room_id == 'None' and not chats.exists():
        return render(request, "chat/room.html", {'user': request.user})
    chat = ChatMessage3.objects.get(id=room_id)
    if request.method == "POST":
        group_chat_form = CreateGroupForm(data=request.POST, files=request.FILES)
        if group_chat_form.is_valid():
            form = group_chat_form.save(commit=False)
            form.save()
            form.user.add(request.user)
    else:
        group_chat_form = CreateGroupForm(instance=chat)
    
    users_in_group = chat.user.all()
    
    return render(request, "chat/room.html", {"room_id": int(room_id),
                                              'user': request.user,
                                              'chats': chats,
                                              'date': timezone.now(),
                                              "group_chat_form": group_chat_form,
                                              "users_in_group": users_in_group})

def change_group(request, room_id):
    chat = ChatMessage3.objects.get(id=room_id)
    if request.method == "POST":
        group_chat_form = CreateGroupForm(data=request.POST, instance=chat, files=request.FILES)
        if group_chat_form.is_valid():
            form = group_chat_form.save(commit=False)
            group_name = group_chat_form.cleaned_data.get('group_name')
            form.save()
            form.user.add(request.user)
            messages.success(request, f'Настройки {group_name} сохранены')
    return redirect(request.META['HTTP_REFERER'])


def user_name(request, user_name, group_id):
    if user_name != "None":
        user_name_2 = request.user
        chat_room = ChatMessage3.objects.filter(user=user_name).filter(user=user_name_2).first()
    else:
        chat_room = ChatMessage3.objects.filter(id=group_id).first()

    if chat_room:
        room_id = chat_room.id
        return redirect('chat:room', room_id=room_id)
    else:
        user_name = User.objects.get(id=user_name)
        create_chat_room = ChatMessage3.objects.create()
        create_chat_room.user.add(user_name_2)
        create_chat_room.user.add(user_name)
        room_id = create_chat_room.id
        return redirect('chat:room', room_id=room_id)
    

def chat_search(request):
    result = []
    if request.method == 'GET':
        query = request.GET.get('search')
        room_id = request.GET.get('room_id')
        if query == '':
            query = 'None'
        result = User.objects.filter(username__icontains = query)
        
        
    does_req_accept_json = request.accepts("application/json")
    is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest" and does_req_accept_json
    if is_ajax_request:
        if room_id:
            html = render_to_string(
                template_name="chat/search_group.html", 
                context={"result": result, "query": query, "room_id": room_id}
            )
        else:
            html = render_to_string(
                template_name="chat/search.html", 
                context={"result": result, "query": query, "user": request.user}
            )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)
    
    return render(request, 'chat/search.html', {'query': query, 'result': result})

        
        
def add_to_group(request, user_name, room_id):
    user = User.objects.get(username=user_name)
    chat_group = ChatMessage3.objects.get(id=room_id)
    chat_group.user.add(user)
    messages.success(request, f'{user} добавлен в {chat_group.group_name}')
    return redirect(request.META['HTTP_REFERER'])

def kickout_from_group(request, user_name, room_id):
    user = User.objects.get(username=user_name)
    chat_group = ChatMessage3.objects.get(id=room_id)
    chat_group.user.remove(user)
    messages.success(request, f'{user} исключен из {chat_group.group_name}')
    return redirect(request.META['HTTP_REFERER'])