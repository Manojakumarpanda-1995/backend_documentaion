from requests.sessions import session
from usermanagement.models import Users
from django.conf import settings
# import re
import os
import sys
import logging
import datetime

from organization.models import Company, UserCompanyRole
from project.models import ProjectUsers, ProjectInfo
from chatbox.models import ChatSession, UsersChannels, ChatHistory

secret = getattr(settings, "SECRET_KEY", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_save_chats(request_data):
    try:
        response = {}

        logs = {
            "Client_IP_Address": request_data["Client_IP_Address"],
            "Remote_ADDR": request_data["Remote_ADDR"],
            "data": {
                "Requested_URL": request_data["Requested_URL"]
            }
        }

        getUsersChannels = UsersChannels.objects.exclude(channel_id=request_data["channel_id"])
        if len(getUsersChannels) == 0:
            logs["data"]["status_message"] = "Invalid channel id."
            response['message'] = "Invalid channel id."
            response["data"] = {"text": request_data["message"],
                                "user": "",
                                "user_id": "",
                                "session_id": "",
                                "message_type": "chat_message"}
            actvity_logs.insert_one(logs)
            return response
        else:
            getUsersChannels = getUsersChannels[0]
            logs["Channel_id"] = getUsersChannels.channel_id

            try:
                getUsers = Users.objects.get(id=request_data["user_id"])
            except:
                response["data"] = {"text": request_data["message"],
                                "user": "",
                                "user_id": "",
                                "session_id": "",
                                "message_type": "chat_message"}
                return response
        getChatSession = ChatSession.objects.filter(session_id=request_data["session_id"])
        if len(getChatSession) == 0:
            logs["data"]["status_message"] = "ChatSession with this id not found."
            response['message'] = "ChatSession with this id not found."
            response["statuscode"] = 400
            response["data"] = {"text": request_data["message"],
                                "user": "",
                                "user_id": "",
                                "session_id": "",
                                "message_type": "chat_message"}

            actvity_logs.insert_one(logs)
            return response
        else:
            getChatSession = getChatSession[0]
            getProjectid = getChatSession.project
            logs["Project_id"] = getChatSession.project.id
        
        # Get all roles
        response = {"message_type": "chat_message"}
        if getUsers and getUsersChannels:
            getChatHistory = ChatHistory.objects.create(user = getUsers,
                                                        project = getProjectid,
                                                        session_id = getChatSession,
                                                        message = request_data["message"])
            response["data"] = {"text": getChatHistory.message,
                                "user": getChatHistory.user.name,
                                "user_id": getChatHistory.user.id,
                                "session_id": getChatHistory.session_id.session_id,
                                "message_type": "chat_message"}
        else:
            response["data"] = {"text": request_data["message"],
                                "user": "",
                                "user_id": "",
                                "session_id": "",
                                "message_type": "chat_message"}

        logs["added_at"] = datetime.datetime.utcnow()
        actvity_logs.insert_one(logs)
        return response

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.info(str(exc_type) + " " + str(fname) + " " + str(exc_tb.tb_lineno) + " " + str(e))
        error_logs.insert_one({
            "error_type": str(exc_type),
            "file_name": str(fname),
            "line_no": str(exc_tb.tb_lineno),
            "error": str(e)
        })
        response["statuscode"] = 500
        return response
