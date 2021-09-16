import requests
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
from chatbox.models import ChatSession, UsersChannels

secret = getattr(settings, "SECRET_KEY", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_mapping_channel_id(request_data):
    try:
        response = {}

        logs = {
            "Client_IP_Address": request_data["Client_IP_Address"],
            "Remote_ADDR": request_data["Remote_ADDR"],
            "data": {
                "Requested_URL": request_data["Requested_URL"]
            }
        }
        getUsers=Users.objects.filter(id=request_data["user_id"])
        if len(getUsers) == 0:
            logs["data"]["status_message"] = 'User with this id not found.'
            response['message'] = 'User with this id not found.'
            response["statuscode"] = 400

            logs["added_at"] = datetime.datetime.utcnow()
            actvity_logs.insert_one(logs)
            return response
            
        getUsers=getUsers[0]
        # Get all roles
        isAuthorized = True
    
        if isAuthorized:
            try:
                getUserChannels=UsersChannels.objects.get(channel_id=
                                                        request_data["channel_id"])
                getUserChannels.user=getUsers
                getUserChannels.save()
                logs["data"]["status_message"] = "Channel id saved successfully."

                response["data"] ={"channel_id": getUserChannels.channel_id,
                                   "user_id": getUserChannels.user.id,
                                   "user_name": getUserChannels.user.name}
                getChatSession = ChatSession.objects.filter(receiver=getUsers)
                if len(getChatSession):
                    response["session_id"] = getChatSession.values("session_id")
                response['message'] = 'Channel id mapped with user {} successfully.'.format(getUsers.email)
                response["statuscode"] = 200
            except Exception as e:
                logs["data"]["status_message"] = 'Invalid channel id.'
                response['message'] = 'Invalid channel id.'
                response["statuscode"] = 400
                logging.info("map chat session==>{}".format(e))
                logs["added_at"] = datetime.datetime.utcnow()
                actvity_logs.insert_one(logs)
                return response
        
        else:
            logs["data"]["status_message"] = 'You are not authorized to list module.'
            response['message'] = 'You are not authorized to list module.'
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
