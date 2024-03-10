from django.shortcuts import render, get_object_or_404, redirect
from authorization.models import User
from chat.models import ChatMessage2, ChatMessage3
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils import timezone


# Create your views here.
def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    #chats = ChatMessage2.objects.filter(user1=request.user) | ChatMessage2.objects.filter(user2=request.user).order_by("-updated")
    chats = ChatMessage3.objects.filter(user=request.user).order_by("-updated")
    
    if room_name == 'None' and chats.exists():
        return render(request, "chat/room.html", {"room_name": chats[0].id, 'user': request.user, "chats": chats})
    elif room_name == 'None' and not chats.exists():
        return render(request, "chat/room.html", {'user': request.user})
    
    
    #is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest"
    #if is_ajax_request:
    #    html_content = render_to_string('chat/includes/included_chat.html', {"room_name": room_name, 'user': request.user,'chats': chats}, request=request)
    #    return JsonResponse({'html_content': html_content})
        #html_content = render_to_string(
        #    template_name='chat/includes/included_chat.html', 
        #    context = {"room_name": room_name, 
        #               'user': request.user, 
        #               'chats': chats}
        #    )
        #data_dict = {"html_from_view": html_content}
        #return JsonResponse(data=data_dict, safe=False)
    #user_name_2 = request.user.username
    #create_chat_room = ChatMessage.objects.create(user1=user_name, user2=user_name_2)
    #print(create_chat_room)
    #else:
    return render(request, "chat/room.html", {"room_name": int(room_name), 'user': request.user, 'chats': chats, 'date': timezone.now()})
    #return render(request, "chat/room_1.html", {"room_name": room_name, 'user': request.user})

#def room(request, user2):
#    user1 = request.user.username
#    return render(request, "chat/room.html", {"user1": user1, "user2": user2})

def user_name(request, user_name):
    user_name_2 = request.user
    #chat_room_1 = ChatMessage2.objects.filter(user1=user_name, user2=user_name_2).first()
    #chat_room_2 = ChatMessage2.objects.filter(user2=user_name, user1=user_name_2).first()
    chat_room = ChatMessage3.objects.filter(user=user_name).filter(user=user_name_2).first()
    
    #if chat_room_1:
    #    room_name = chat_room_1.id
    #    return redirect('chat:room', room_name=room_name)
    #elif chat_room_2:
    #    room_name = chat_room_2.id
    #    #room(request, room_name)
    #    return redirect('chat:room', room_name=room_name)
    if chat_room:
        room_name = chat_room.id
        return redirect('chat:room', room_name=room_name)
    else:
        user_name = User.objects.get(id=user_name)
        #user_name_2 = User.objects.get(id=user_name_2.id)
        print(user_name)
        print(user_name_2)
        #create_chat_room = ChatMessage2.objects.create(user1=user_name, user2=user_name_2)
        create_chat_room = ChatMessage3.objects.create()
        create_chat_room.user.add(user_name_2)
        create_chat_room.user.add(user_name)
        
        room_name = create_chat_room.id
        return redirect('chat:room', room_name=room_name)
    

def chat_search(request):
    result = []
    if request.method == 'GET':
        query = request.GET.get('search')
        if query == '':
            query = 'None'
        result = User.objects.filter(username__icontains = query)
        
        
        
    does_req_accept_json = request.accepts("application/json")
    is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest" and does_req_accept_json
    if is_ajax_request:
        html = render_to_string(
            template_name="chat/search.html", 
            context={"result": result, "query":query}
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)
    
    return render(request, 'chat/search.html', {'query': query, 'result': result})
