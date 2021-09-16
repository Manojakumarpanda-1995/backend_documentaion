from usermanagement.models import Users
from django.conf import settings
# import re
import os
import sys
import logging
import datetime
from django.db.models import Q
from organization.models import Company, UserCompanyRole
from project.models import ProjectUsers
from chatbox.models import ChatHistory, ChatSession

secret = getattr(settings, "SECRET_KEY", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_list_chat_history(request_data, token):
    try:
        response = {}

        logs = {
            "Client_IP_Address": request_data["Client_IP_Address"],
            "Remote_ADDR": request_data["Remote_ADDR"],
            "data": {
                "Requested_URL": request_data["Requested_URL"]
            }
        }

        curr_user = Users.objects.filter(token=token)
        if len(curr_user) == 0:
            logs["data"]["status_message"] = "Invalid Token."
            response['message'] = "Invalid Token."
            response["statuscode"] = 400

            actvity_logs.insert_one(logs)
            return response
        else:
            curr_user = curr_user[0]
            logs["User"] = curr_user.id

            # Get UserCompanyRole
            getUserCompanyRole = UserCompanyRole.objects.filter(user=curr_user,
                                                                user__active=True,
                                                                company__active=True,
                                                                role__active=True,
                                                                isActive=True)

        # Get all roles


        allRoles = []
        for user in getUserCompanyRole:
            if user.role.role_name.upper() not in allRoles:
                allRoles.append(user.role.role_name.upper())

        if "SUPER-USER" in allRoles:
            Session_id = []
            getChatSession = ChatSession.objects.filter(Q(sender__user__user__id=request_data["user_id"])
                                                        |Q(receiver__id=request_data["user_id"]))
            if len(getChatSession) == 0:
                response["data"] = [{"session_id":"","data":[]}]
                response["message"] = "Chat session listed successfully."
                response["statuscode"] = 200
                return response
            displayData = {}
            for chatsession in getChatSession:
                getChatHistory = ChatHistory.objects.filter(session_id=chatsession,
                                                            project__isActive=True)
                if chatsession.session_id not in Session_id: 
                    displayData[chatsession.session_id] = []
                    Session_id.append(chatsession.session_id)
                for chathistory in getChatHistory:

                    displayData[chatsession.session_id].append({
                        "id": chathistory.id,
                        "user_id": chathistory.user.id,
                        "user_name": chathistory.user.name,
                        "session_id": chathistory.session_id.session_id,
                        "project_id": chathistory.project.id,
                        "chat_message": chathistory.message,
                        "status": chathistory.status,
                        "read": chathistory.read,
                        "project_status": chathistory.project.isActive,
                        "time_stamp": chathistory.time_stamp,
                        "isEditable": True
                    })
                    displayData["sender_id"] = chathistory.user.id
                    displayData["sender_name"] = chathistory.user.name
                    getReceiver = ChatSession.objects.filter(session_id=
                                                             chathistory.session_id.session_id)
                    if getReceiver[0].sender.user.user.id == chathistory.user.id:
                        displayData["receiver_id"] = getReceiver[0].receiver.id
                        displayData["receiver_name"] = getReceiver[0].receiver.name
                    elif getReceiver[0].receiver.id == chathistory.user.id:
                        displayData["sender_id"] = getReceiver[0].sender.user.user.id
                        displayData["sender_name"] = getReceiver[0].sender.user.user.name
        elif "COMPANY-ADMIN" in allRoles:
            Session_id = []
            getChatSession = ChatSession.objects.filter(Q(sender__user__user__id=request_data["user_id"])
                                                        |Q(receiver__id=request_data["user_id"]))
            if len(getChatSession) == 0:
                response["data"] = [{"session_id":"","data":[]}]
                response["message"] = "Chat session listed successfully."
                response["statuscode"] = 200
                return response
            displayData = {}
            for chatsession in getChatSession:
                getChatHistory = ChatHistory.objects.filter(session_id=chatsession,
                                                            project__isActive=True)
                
                if chatsession.session_id not in Session_id: 
                    displayData[chatsession.session_id] = []
                    Session_id.append(chatsession.session_id)
                    
                for chathistory in getChatHistory:

                    displayData[chatsession.session_id].append({
                        "id": chathistory.id,
                        "user_id": chathistory.user.id,
                        "user_name": chathistory.user.name,
                        "session_id": chathistory.session_id.session_id,
                        "project_id": chathistory.project.id,
                        "chat_message": chathistory.message,
                        "status": chathistory.status,
                        "read": chathistory.read,
                        "project_status": chathistory.project.isActive,
                        "time_stamp": chathistory.time_stamp,
                        "isEditable": True
                    })
                    displayData["sender_id"] = chathistory.user.id
                    displayData["sender_name"] = chathistory.user.name
                    getReceiver = ChatSession.objects.filter(session_id=
                                                             chathistory.session_id.session_id)
                    if getReceiver[0].sender.user.user.id == chathistory.user.id:
                        displayData["receiver_id"] = getReceiver[0].receiver.id
                        displayData["receiver_name"] = getReceiver[0].receiver.name
                    elif getReceiver[0].receiver.id == chathistory.user.id:
                        displayData["sender_id"] = getReceiver[0].sender.user.user.id
                        displayData["sender_name"] = getReceiver[0].sender.user.user.name
                        
        elif "PROJECT-ADMIN" in allRoles:
            Session_id = []
            getChatSession = ChatSession.objects.filter(Q(sender__user__user__id=request_data["user_id"])
                                                        |Q(receiver__id=request_data["user_id"]))
            if len(getChatSession) == 0:
                response["data"] = [{"session_id":"","data":[]}]
                response["message"] = "Chat session listed successfully."
                response["statuscode"] = 200
                return response
            displayData = {}
            for chatsession in getChatSession:
                getChatHistory = ChatHistory.objects.filter(session_id=chatsession,
                                                            project__isActive=True)

                if chatsession.session_id not in Session_id: 
                    displayData[chatsession.session_id] = []
                    Session_id.append(chatsession.session_id)
                for chathistory in getChatHistory:
                    displayData[chatsession.session_id].append({
                        "id": chathistory.id,
                        "user_id": chathistory.user.id,
                        "user_name": chathistory.user.name,
                        "session_id": chathistory.session_id.session_id,
                        "project_id": chathistory.project.id,
                        "chat_message": chathistory.message,
                        "status": chathistory.status,
                        "read": chathistory.read,
                        "project_status": chathistory.project.isActive,
                        "time_stamp": chathistory.time_stamp,
                        "isEditable": True
                    })
                    displayData["sender_id"] = chathistory.user.id
                    displayData["sender_name"] = chathistory.user.name
                    getReceiver = ChatSession.objects.filter(session_id=
                                                             chathistory.session_id.session_id)
                    if getReceiver[0].sender.user.user.id == chathistory.user.id:
                        displayData["receiver_id"] = getReceiver[0].receiver.id
                        displayData["receiver_name"] = getReceiver[0].receiver.name
                    elif getReceiver[0].receiver.id == chathistory.user.id:
                        displayData["sender_id"] = getReceiver[0].sender.user.user.id
                        displayData["sender_name"] = getReceiver[0].sender.user.user.name
                        
                    
        else:
            logs["data"]["status_message"] = 'You are not authorized to list module.'
            response['message'] = 'You are not authorized to list module.'
            response["statuscode"] = 400
        data = []
        for key,value in displayData.items():
            temp_dict = {}
            if key in ["sender_id", "sender_name", "receiver_id", "receiver_name"]:
                pass
            else:
                temp_dict["sender_id"] = displayData.get("sender_id")
                temp_dict["sender_name"] = displayData.get("sender_name")
                temp_dict["receiver_id"] = displayData.get("receiver_id")
                temp_dict["receiver_name"] = displayData.get("receiver_name")
                temp_dict["session_id"] = key
                temp_dict["data"] = value
                data.append(temp_dict)

        response["data"] = data
        response['message_type'] = 'chat_history'
        response['is_data'] = True if len(data) else False
        response["statuscode"] = 200
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
