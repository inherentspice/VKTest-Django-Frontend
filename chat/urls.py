from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='chat'),
    path('<str:room_name>/<str:user_name>/<int:role>', views.room_view, name='chat-room'),
    path('<str:room_name>/<str:user_name>/<int:role>/results', views.get_results, name='results'),
    path('<str:room_name>/<str:user_name>/<int:role>/<str:old_question>', views.question_view, name='question'),
]
