from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', HomePageView.as_view(), name='home'), 
    path('chat/', ChatView.as_view(), name='chat'),  
    path('chat/api/', csrf_exempt(ChatQueryAPI.as_view()), name='chat_query_api'),
    path('chat/new-session/', NewSessionView.as_view(), name='new_session'),

]
