from django.shortcuts import render, get_object_or_404, redirect
from authorization.models import User
from chat.models import ChatMessage2

# Create your views here.
def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    #user_name_2 = request.user.username
    #create_chat_room = ChatMessage.objects.create(user1=user_name, user2=user_name_2)
    #print(create_chat_room)
   
    
    return render(request, "chat/room.html", {"room_name": room_name, 'user': request.user})

#def room(request, user2):
#    user1 = request.user.username
#    return render(request, "chat/room.html", {"user1": user1, "user2": user2})

def user_name(request, user_name):
    user_name_2 = request.user
    chat_room_1 = ChatMessage2.objects.filter(user1=user_name, user2=user_name_2).first()
    chat_room_2 = ChatMessage2.objects.filter(user2=user_name, user1=user_name_2).first()
    if chat_room_1:
        room_name = chat_room_1.id
        return redirect('chat:room', room_name=room_name)
    elif chat_room_2:
        room_name = chat_room_2.id
        #room(request, room_name)
        return redirect('chat:room', room_name=room_name)
    else:
        user_name = User.objects.get(id=user_name)
        #user_name_2 = User.objects.get(id=user_name_2.id)
        print(user_name)
        print(user_name_2)
        create_chat_room = ChatMessage2.objects.create(user1=user_name, user2=user_name_2)
        
        room_name = create_chat_room.id
        return redirect('chat:room', room_name=room_name)
    

def chat_search(request):
    result = []
    if request.method == 'GET':
        query = request.GET.get('search')
        if query == '':
            query = 'None'
        result = User.objects.filter(username__icontains = query)
        return render(request, 'chat/search.html', {'query': query, 'result': result})