from unicodedata import name
from django.shortcuts import render
import requests
from chat.models import Room, User


def index_view(request):
    return render(request, 'index.html', {
        'rooms': Room.objects.all(),
        'users': User.objects.all(),
    })


def room_view(request, room_name, user_name, role):
    room_query = Room.objects.filter(name=room_name)
    if room_query.exists():
        chat_room = Room.objects.get(name=room_name)
    else:
        question_url = "https://vktest-kr575za6oa-uw.a.run.app/question"
        question_response = requests.get(question_url).json()['question']
        chat_room = Room.objects.create(name=room_name, question=question_response)

    if role % 2 == 0:
        role = True
    else:
        role = False

    user = User.objects.create(username=user_name, role=role)

    return render(request, 'room.html', {
        'room': chat_room,
        'user': user,
    })

def question_view(request, room_name, user_name, old_question, role):
    old_question += '?'
    room_query = Room.objects.filter(name=room_name, question = old_question)
    if room_query.exists():
        Room.objects.filter(name=room_name, question=old_question).delete()
        question_url = "https://vktest-kr575za6oa-uw.a.run.app/question"
        question_response = requests.get(question_url).json()['question']
        chat_room = Room.objects.create(name=room_name, question=question_response)
    else:
        chat_room = Room.objects.get(name=room_name)

    if role % 2 == 0:
        role = True
    else:
        role = False

    user = User.objects.create(username=user_name, role=role)

    return render(request, 'room.html', {
        'room': chat_room,
        'user': user,
    })
