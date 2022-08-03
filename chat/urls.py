from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='chat'),
    path('<str:room_name>/<str:user_name>/<int:role>', views.room_view, name='chat-room'),
    path('<str:room_name>/<str:user_name>/<str:old_question>/<int:role>', views.question_view, name='question'),

]
