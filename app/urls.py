from django.contrib import admin
from django.urls import path

from app.views import HomePage, SaveStream, SaveAudio

urlpatterns = [
    path('', HomePage.as_view(), name='homepage'),
    path('save-stream/', SaveStream.as_view(), name='save_stream'),
    path('save-audio/', SaveAudio.as_view(), name='save_audio'),
]
