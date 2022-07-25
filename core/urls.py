from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index_view, name='home'),
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
]
