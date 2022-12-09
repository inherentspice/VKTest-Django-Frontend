from unicodedata import name
from django.shortcuts import render
import requests
from chat.models import Room, User
import random

# List of subjective questions with specific examples
questions = ["What do you think about the current state of politics?",
             "How do you feel about the pandemic?",
             "What was your experience with traveling to a new country like?",
             "What is your opinion on climate change?",
             "How do you handle stress?",
             "What do you believe about the existence of extraterrestrial life?",
             "What are your thoughts on social media?",
             "What is your perspective on the education system?",
             "What is your stance on gun control?",
             "What is your view on the importance of arts and culture?"]


def index_view(request):
    return render(request, 'roomselection.html', {
        'rooms': Room.objects.all(),
        'users': User.objects.all(),
    })


def room_view(request, room_name, user_name, role):
    room_query = Room.objects.filter(name=room_name)
    if room_query.exists():
        chat_room = Room.objects.get(name=room_name)
    else:
        try:
            # Make the request to the API
            question_url = "https://vktest-kr575za6oa-uw.a.run.app/question"
            question_response = requests.get(question_url).json()['question']

        except:
            # Handle the error by selecting a random question from the list
            question_response = random.choice(questions)
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

def question_view(request, room_name, user_name, role, old_question):
    old_question += '?'
    room_query = Room.objects.filter(name=room_name, question = old_question)
    if room_query.exists():
        Room.objects.filter(name=room_name, question=old_question).delete()
        try:
            # Make the request to the API
            question_url = "https://vktest-kr575za6oa-uw.a.run.app/question"
            question_response = requests.get(question_url).json()['question']

        except:
            # Handle the error by selecting a random question from the list
            question_response = random.choice(questions)
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

def get_results(request, room_name, user_name, role):
    chat_room = Room.objects.get(name=room_name)
    if role % 2 == 0:
        role = True
    else:
        role = False

    user = User.objects.create(username=user_name, role=role)

    return render(request, 'results.html', {
        'room': chat_room,
        'user': user,
    })
