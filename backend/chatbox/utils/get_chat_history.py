from usermanagement.models import Users
from django.conf import settings
# import re
import os
import sys
import logging
import datetime

from organization.models import Company, UserCompanyRole
from project.models import ProjectInfo, ProjectUsers
from chatbox.models import ChatSession,ChatHistory

secret = getattr(settings, "SECRET_KEY", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_get_chat_history(request_data):
    try:
        response = {}

        logs = {
            "Client_IP_Address": request_data["Client_IP_Address"],
            "Remote_ADDR": request_data["Remote_ADDR"],
            "data": {
                "Requested_URL": request_data["Requested_URL"]
            }
        }
        getSender = ProjectUsers.objects.filter(user__user__id=request_data["sender"],
                                                project__id=request_data["project"])
        getReceiver = Users.objects.filter(id=request_data["receiver"])
        
        if len(getSender) == 0:
            # When the project admin act as receiver
            getReceiver = Users.objects.filter(id=request_data["sender"])
            if len(getReceiver) == 0:
                logs["data"]["status_message"] = "No User with this sender id found."
                response['message'] = "No User with this sender id found."
                actvity_logs.insert_one(logs)
                return response

        elif len(getReceiver) == 0:
            logs["data"]["status_message"] = "No User with this receiver id found."
            response['message'] = "No User with this receiver id found."
            response["statuscode"] = 400
            actvity_logs.insert_one(logs)
            return response

        # When the project admin act as receiver
        getProjectUser = ProjectUsers.objects.filter(user__user__id=request_data["receiver"],
                                                project__id=request_data["project"])
        if len(getProjectUser) == 1:
            getSender = getProjectUser
        
        getProjectInfo=ProjectInfo.objects.filter(id=request_data["project"])
        if len(getProjectInfo) == 0: 
            logs["data"]["status_message"] = "No Project found with this information."
            response['message'] = "No Project found with this information."
            response["statuscode"] = 400

            actvity_logs.insert_one(logs)
            return response
        
        if len(getSender) and len(getReceiver) and len(getProjectInfo):
            getChatsessions = ChatSession.objects.filter(sender=getSender[0],
                                                         receiver=getReceiver[0],
                                                         project=getProjectInfo[0])

            displayData = {}
            for chatsession in getChatsessions:
                displayData[chatsession.session_id] = []
                getChatHistries=ChatHistory.objects.filter(session_id=chatsession)
                for history in getChatHistries:
                    displayData[chatsession.session_id].append({
                        "id": history.id,
                        "user_id":history.user.id,
                        "sender_name": history.user.name,
                        "sender_email": history.user.email,
                        "project_name": chatsession.project.name,
                        "project_id": chatsession.project.project_id,
                        "chat_message": history.message,
                        "status": history.status,
                        "project_status": chatsession.project.isActive,
                        "created_at": history.time_stamp,
                        "read": history.read
                    })
            # response["data"] = displayData
        else:
            logs["data"]["status_message"] = 'You are not authorized to list module.'
            response['message'] = 'You are not authorized to list module.'
            response["statuscode"] = 400
         
        logs["data"]["status_message"] = "Chat history listed successfully."

        data = []
        for key,value in displayData.items():
            # data.append({"session_id":key,"data":value})
            response["session_id"] = key
            response["data"] = value
            data.extend(value)
        response['message_type'] = 'chat_history'
        response['is_data'] = True if len(data) else False
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
