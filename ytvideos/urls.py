# /Users/atomshock/PycharmProjects/tbProject/ytvideos/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('channels/<str:channel_id>/videos/', views.get_channel_videos_metadata, name='channel-videos'),
]
