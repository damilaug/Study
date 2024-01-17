from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from datetime import datetime
from .models import Room,Topic, Message
from .forms import RoomForm, UserForm
from django.db.models import Q

# Create your views here.

# rooms = [
#     {"id": 1, "name": "Full stack web dev roadmap"},
#     {"id": 2, "name": "Learn frontend web development"},
#     {"id": 3, "name": "Learn backend web development"},
#     {"id": 4, "name": "Learn APIs"}
# ]

def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    rooms = Room.objects.filter(
         Q(topic__name__icontains=q) |
         Q(name__icontains=q) |
         Q(description__icontains=q)
                                ) 
    topics = Topic.objects.all()[0:5]
    rooms_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {"rooms": rooms, "topics": topics, "rooms_count":rooms_count, "room_messages": room_messages}
    return render(request, 'page/index.html', context)

def loginPage(request):
     page = 'login'
     if request.user.is_authenticated:
          return redirect('index')
     if request.method == 'POST':
          username = request.POST.get('username')
          password = request.POST.get('password')
          try:
               user = User.objects.get(username=username)
          
          except User.DoesNotExist:
               messages.error(request, "This user does not exist")
          
          user = authenticate(request, username=username, password=password)
          if user is not None:
               login(request, user)
               return redirect("index")
          else:
               messages.error(request, "Incorrect username or password")
     context = {'page': page}
     return render(request, 'page/register_login.html', context)

def LogoutUser(request):
     logout(request)
     return redirect('index')

def registerPage(request):
     form = UserCreationForm()
     if request.method == 'POST':
          form = UserCreationForm(request.POST)
          if form.is_valid():
               user = form.save(commit=False)
               user.username = user.username.capitalize()
               user.save()
               login(request, user)
               return redirect('index')
          else:
               messages.error(request, 'An error occured during registration')
     context = {'form': form}
     return render(request, 'page/register_login.html', context)
def services(request, pk):
    # room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    room = Room.objects.get(id=pk)
    context = {"room":room}
    return render(request, 'page/services.html', context)

def about_us(request):
        return render(request, 'page/about.html')

def room(request, pk):
     room = Room.objects.get(id=pk)
     room_messages = room.message_set.all().order_by('-created')
     partcipants = room.participants.all()
     if request.method == 'POST':
          message = Message.objects.create(
               user = request.user,
               room = room,
               body = request.POST.get('body'),
          )
          room.participants.add(request.user)
          return redirect('room', pk=room.id)
     context = {'room': room, 'room_messages': room_messages, 'participants':partcipants}
     return render(request, 'page/room.html', context)

def userProfile(request, pk):
     user = User.objects.get(id=pk)
     rooms = user.room_set.all()
     room_messages = user.message_set.all()
     topics = Topic.objects.all()
     context = {'user': user, 'rooms': rooms, 'room_messages':room_messages, 'topics':topics }
     return render(request, 'page/profile.html', context)

@login_required(login_url ='login')
def createRoom(request):
     form = RoomForm()
     topics = Topic.objects.all()
     if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)

        Room.objects.create(
             host = request.user,
             topic = topic,
             name = request.POST.get('name'),
             description = request.POST.get('description')
        )
        return redirect("index")
     #    form = RoomForm(request.POST)
     #    if form.is_valid():
     #         room = form.save(commit=False)
     #         room.host = request.user
     #         room.save()
     
     context = {"form": form, "topics": topics}
     return render(request, 'page/room_form.html', context)

def updateRoom(request, pk):
     room = Room.objects.get(id=pk)
     form = RoomForm(instance=room)
     topics = Topic.objects.all()
     if request.user != room.host:
          return HttpResponse("You are not allowed to edit this room")
     if request.method == 'POST':
          topic_name = request.POST.get('topic')
          topic, created = Topic.objects.get_or_create(name = topic_name)
          room.name = request.POST.get('name')
          room.topic = topic
          room.description = request.POST.get('description')
          room.save()
          form = RoomForm(request.POST, instance = room)
          if form.is_valid():
               form.save()
               return redirect("index")
     context = {"form": form, "topics": topics}
     return render(request, 'page/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
     room = Room.objects.get(id=pk)
     if request.user != room.host:
          return HttpResponse("You are not allowed to delete this room")
     if request.method == 'POST':
          room.delete()
          return redirect('index')
     return render(request, "page/delete.html", {"obj":room})

@login_required(login_url='login')
def deleteMessage(request, pk):
     message = Message.objects.get(id=pk)
     if request.user != message.user:
          return HttpResponse("You are not allowed to delete this message")
     if request.method == 'POST':
          message.delete()
          return redirect('index')
     return render(request, "page/delete.html", {"obj":message})

@login_required(login_url='login')
def updateUser(request):
     user = request.user

     if request.method == 'POST':
          form = UserForm(request.POST, instance=user)
          if form.is_valid():
               form.save()
               return redirect('user-profile', pk=user.id)

     form = UserForm(instance = user)
     return render(request, "page/update-user.html", {'form': form})

def topicsPage(request):
     q = request.GET.get('q') if request.GET.get('q') != None else ""
     topics = Topic.objects.filter(name__icontains=q)
     return render(request, "page/topics.html", {'topics': topics}) 

def activityPage(request):
     room_messages = Message.objects.all()
     return render(request, "page/activity.html", {'room_messages': room_messages})