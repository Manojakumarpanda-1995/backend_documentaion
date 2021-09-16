import logging
import os

import requests
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework import schemas
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.schemas import AutoSchema

from chatbox.utils.list_chat_history import func_list_chat_history
from chatbox.utils.get_chat_history import func_get_chat_history
from chatbox.utils.get_chat_room import func_get_chat_room
from chatbox.utils.save_channel_id import func_save_channel_id
from chatbox.utils.mapping_channel_id import func_mapping_channel_id
from chatbox.utils.remove_channel_id import func_remove_channel_id
from chatbox.utils.list_channel_id_bysession import \
    func_list_channel_id_bysession
from chatbox.utils.list_channel_id_by_user import func_list_channel_id_by_user
from chatbox.utils.save_chats import func_save_chats

class list_chat_history(APIView):
    permission_classes=(AllowAny,)
    allowed_methods=("POST",)
    # schema=AutoSchema(manual_fields=List_ChatHistory_Schema().get_manual_fields())

    def post(self,request):
        request_data = request.data
        newInfo = {
            "Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
            # #"Requested_URL": request.META["REQUEST_URI"],
                "Requested_URL": request.META["PATH_INFO"],
            "Requested_URL": request.META["PATH_INFO"],
            "Remote_ADDR": request.META["REMOTE_ADDR"]
        }
        request_data = {**request_data, **newInfo}
        token = request.META["HTTP_AUTHORIZATION"]
        response = func_list_chat_history(request_data,token)
        return Response(response)

    
class get_chat_room(APIView):
    permission_classes=(AllowAny,)
    allowed_methods=("POST",)
    # schema=AutoSchema(manual_fields=List_ChatHistory_Schema().get_manual_fields())

    def post(self,request):
        request_data = request.data
        newInfo = {
            "Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
            # #"Requested_URL": request.META["REQUEST_URI"],
                "Requested_URL": request.META["PATH_INFO"],
            "Requested_URL": request.META["PATH_INFO"],
            "Remote_ADDR": request.META["REMOTE_ADDR"]
        }
        request_data = {**request_data, **newInfo}
        token = request.META["HTTP_AUTHORIZATION"]
        response = func_get_chat_room(request_data,token)
        return Response(response)

    
class get_chat_history(APIView):
    permission_classes=(AllowAny,)
    allowed_methods=("POST",)
    # schema=AutoSchema(manual_fields=List_ChatHistory_Schema().get_manual_fields())

    def post(self,request):
        request_data = request.data
        newInfo = {
            "Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
            # #"Requested_URL": request.META["REQUEST_URI"],
                "Requested_URL": request.META["PATH_INFO"],
            "Requested_URL": request.META["PATH_INFO"],
            "Remote_ADDR": request.META["REMOTE_ADDR"]
        }
        request_data = {**request_data, **newInfo}
        response = func_get_chat_history(request_data)
        return Response(response)


class save_channel_id(APIView):
    permission_classes=(AllowAny,)
    allowed_methods=("POST",)
    # schema=AutoSchema(manual_fields=List_ChatHistory_Schema().get_manual_fields())

    def post(self,request):
        request_data = request.data
        newInfo = {
            "Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
            # #"Requested_URL": request.META["REQUEST_URI"],
                "Requested_URL": request.META["PATH_INFO"],
            "Requested_URL": request.META["PATH_INFO"],
            "Remote_ADDR": request.META["REMOTE_ADDR"]
        }
        request_data = {**request_data, **newInfo}
        response = func_save_channel_id(request_data)
        return Response(response)

    
class save_chats(APIView):
    permission_classes=(AllowAny,)
    allowed_methods=("POST",)
    # schema=AutoSchema(manual_fields=List_ChatHistory_Schema().get_manual_fields())

    def post(self,request):
        request_data = request.data
        newInfo = {
            "Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
            # #"Requested_URL": request.META["REQUEST_URI"],
                "Requested_URL": request.META["PATH_INFO"],
            "Requested_URL": request.META["PATH_INFO"],
            "Remote_ADDR": request.META["REMOTE_ADDR"]
        }
        request_data = {**request_data, **newInfo}
        response = func_save_chats(request_data)
        return Response(response)

    
class list_channel_id_bysession(APIView):
    permission_classes=(AllowAny,)
    allowed_methods=("POST",)
    # schema=AutoSchema(manual_fields=List_ChatHistory_Schema().get_manual_fields())

    def post(self,request):
        request_data = request.data
        newInfo = {
            "Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
            # #"Requested_URL": request.META["REQUEST_URI"],
                "Requested_URL": request.META["PATH_INFO"],
            "Requested_URL": request.META["PATH_INFO"],
            "Remote_ADDR": request.META["REMOTE_ADDR"]
        }
        request_data = {**request_data, **newInfo}
        response = func_list_channel_id_bysession(request_data)
        return Response(response)

    
class list_channel_id_by_user(APIView):
    permission_classes=(AllowAny,)
    allowed_methods=("POST",)
    # schema=AutoSchema(manual_fields=List_ChatHistory_Schema().get_manual_fields())

    def post(self,request):
        request_data = request.data
        newInfo = {
            "Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
            # #"Requested_URL": request.META["REQUEST_URI"],
                "Requested_URL": request.META["PATH_INFO"],
            "Requested_URL": request.META["PATH_INFO"],
            "Remote_ADDR": request.META["REMOTE_ADDR"]
        }
        request_data = {**request_data, **newInfo}
        response = func_list_channel_id_by_user(request_data)
        return Response(response)

    
class mapping_channel_id(APIView):
    permission_classes=(AllowAny,)
    allowed_methods=("POST",)
    # schema=AutoSchema(manual_fields=List_ChatHistory_Schema().get_manual_fields())

    def post(self,request):
        request_data = request.data
        newInfo = {
            "Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
            # #"Requested_URL": request.META["REQUEST_URI"],
                "Requested_URL": request.META["PATH_INFO"],
            "Requested_URL": request.META["PATH_INFO"],
            "Remote_ADDR": request.META["REMOTE_ADDR"]
        }
        request_data = {**request_data, **newInfo}
        response = func_mapping_channel_id(request_data)
        return Response(response)
    
class remove_channel_id(APIView):
    permission_classes=(AllowAny,)
    allowed_methods=("POST",)
    # schema=AutoSchema(manual_fields=List_ChatHistory_Schema().get_manual_fields())

    def post(self,request):
        request_data = request.data
        newInfo = {
            "Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
            # #"Requested_URL": request.META["REQUEST_URI"],
                "Requested_URL": request.META["PATH_INFO"],
            "Requested_URL": request.META["PATH_INFO"],
            "Remote_ADDR": request.META["REMOTE_ADDR"]
        }
        request_data = {**request_data, **newInfo}
        response = func_remove_channel_id(request_data)
        return Response(response)
