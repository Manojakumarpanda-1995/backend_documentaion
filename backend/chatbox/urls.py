from django.urls import path
from . import views

app_name = "chatbox"

urlpatterns = [
    path("list-chat-history", views.list_chat_history.as_view(), name="list-chat-history"),
    path("get-chat-room", views.get_chat_room.as_view(), name="get-chat-room"),
    path("get-chat-history", views.get_chat_history.as_view(), name="get-chat-history"),
    path("save-chats", views.save_chats.as_view(), name="save-chats"),
    path("save-channel-id", views.save_channel_id.as_view(), name="save-channel-id"),
    path("list-channel-id", views.list_channel_id_bysession.as_view(), name="list-channel-id"),
    path("get-channel-id", views.list_channel_id_by_user.as_view(), name="get-channel-id"),
    path("map-channel-id", views.mapping_channel_id.as_view(), name="map-channel-id"),
    path("remove-channel-id", views.remove_channel_id.as_view(), name="remove-channel-id"),
]
