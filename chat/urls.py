from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
path('chats/', views.ChatSessionView.as_view()),
path('chats/<uri>/', views.ChatSessionView.as_view()),
path('chats/<uri>/messages/', views.ChatSessionMessageView.as_view()),
path('chat/', views.indexChat, name='indexChat'),
path('chat/<str:room_name>/', views.room, name='room'),
]