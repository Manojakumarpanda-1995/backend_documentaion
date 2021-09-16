from usermanagement.models import Users
from django.conf import settings
import uuid
import os
import sys
import logging
import datetime

from organization.models import Company, UserCompanyRole
from project.models import ProjectInfo, ProjectUsers
from chatbox.models import ChatSession

secret = getattr(settings, "SECRET_KEY", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_get_chat_room(request_data, token):
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
        isAuthorized = False
        displayData = []
        allRoles = []
        for user in getUserCompanyRole:
            if user.role.role_name.upper() not in allRoles:
                allRoles.append(user.role.role_name.upper())

        if "SUPER-USER" in allRoles:
            isAuthorized = True
            
        elif "COMPANY-ADMIN" in allRoles:
            isAuthorized = True

        elif "PROJECT-ADMIN" in allRoles:
            isAuthorized = True

        else:
            logs["data"]["status_message"] = 'You are not authorized to get group id.'
            response['message'] = 'You are not authorized to get group id.'
            response["statuscode"] = 400

        # To validate that the sender user is valid
        getUser = Users.objects.filter(id=request_data["sender_id"],
                                       active=True)
        
        if len(getUser) == 0:
            logs["data"]["status_message"] = "User with this detail not found."

            response['message'] = "User with this detail not found."
            response["statuscode"] = 400
        else:
            getUser = getUser[0]
            
        # To validate that the receiver user is valid
        getReceiver = Users.objects.filter(id=request_data["receiver_id"],
                                       active=True)
        
        if len(getReceiver) == 0:
            logs["data"]["status_message"] = "User with this detail not found."

            response['message'] = "User with this detail not found."
            response["statuscode"] = 400
        else:
            getReceiver = getReceiver[0]
            
        # To validate that the project
        getProjectInfo = ProjectInfo.objects.filter(id=request_data["project_id"],
                                                     isActive=True)
        if len(getProjectInfo) == 0:
            logs["data"]["status_message"] = "Project with this detail not found."

            response['message'] = "Project with this detail not found."
            response["statuscode"] = 400
        else:
            getProjectInfo = getProjectInfo[0]

        # To validate that the company
        getCompany = Company.objects.filter(id=request_data["client_id"],
                                             active=True)
        if len(getCompany) == 0:
            logs["data"]["status_message"] = "Company with this detail not found."

            response['message'] = "Company with this detail not found."
            response["statuscode"] = 400
        else:
            getCompany = getCompany[0]

        if isAuthorized:

            getProjectUser = ProjectUsers.objects.filter(user__user=getUser,
                                                         project=getProjectInfo)

            if len(getProjectUser) == 0:
                logs["data"]["status_message"] = "You are not authorized group id."

                response['message'] = "You are not authorized group id."
                response["statuscode"] = 400
                actvity_logs.insert_one(logs)
                return response

            apiParamsInfo={}
            apiParamsInfo["sender"] = getProjectUser[0]
            apiParamsInfo["receiver"] = getReceiver
            apiParamsInfo["company"] = getCompany
            apiParamsInfo["project"] = getProjectInfo
            apiParamsInfo["created_by"] = curr_user
            apiParamsInfo["updated_by"] = curr_user

            getChatSession,created = ChatSession.objects.get_or_create(**apiParamsInfo)
            if getChatSession.session_id is None:
                getChatSession.session_id = uuid.uuid4().hex
                getChatSession.save()
            data={}
            data["id"] = getChatSession.id
            data["session_id"] = getChatSession.session_id
            data["sender"] = getChatSession.sender.id
            data["receiver"] = getChatSession.receiver.id
            data["company"] = getChatSession.company.id
            data["project"] = getChatSession.project.id
            data["created_by"] = curr_user.id
            data["updated_by"] = curr_user.id
            response["data"] = data
            logs["data"]["status_message"] = "Chat group id fetched successfully."
            response['message'] = 'Chat group id fetched successfully.'
            response["statuscode"] = 200
        else:
            logs["data"]["status_message"] = 'You cannot fetch chat session.'
            response['message'] = 'You cannot fetch chat session.'
            response["statuscode"] = 400

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
