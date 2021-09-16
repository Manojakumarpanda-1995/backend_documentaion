from requests.sessions import session
from usermanagement.models import Users
from django.conf import settings
# import re
import os
import sys
import logging
import datetime

from chatbox.models import ChatSession, UsersChannels

secret = getattr(settings, "SECRET_KEY", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_list_channel_id_bysession(request_data):
    try:
        response = {}

        logs = {
            "Client_IP_Address": request_data["Client_IP_Address"],
            "Remote_ADDR": request_data["Remote_ADDR"],
            "data": {
                "Requested_URL": request_data["Requested_URL"]
            }
        }

        getChatSession = ChatSession.objects.filter(session_id=request_data["session_id"]).exclude(
                                                    receiver=None)
        if len(getChatSession) == 0:
            logs["data"]["status_message"] = "Invalid session id."
            response['message'] = "Invalid session id."
            response["statuscode"] = 400
            response["data"] = []
            actvity_logs.insert_one(logs)
            return response
        else:
            getChatSession = getChatSession
            # logging.info("Chatsession==>{}".format(getChatSession.values()))
            logs["Session_id"] = getChatSession[0].id

        
        getUsers=[]
        for chatsession in getChatSession:
            if chatsession.receiver.id  not in getUsers:
                getUsers.append(chatsession.receiver.id)
            if chatsession.sender.user.user.id not in getUsers:
                getUsers.append(chatsession.sender.user.user.id)

        # logging.info("GetUsers==>{}".format(getUsers))
        getUsersChannel=UsersChannels.objects.filter(user__id__in=getUsers)
        Channel_ids=[]
        if len(getUsersChannel) != 0:

            for userchannel in getUsersChannel:
                Channel_ids.append({"channel_id": userchannel.channel_id,
                                    "user_id": userchannel.user.id
                                    })
        else:
            logs["data"]["status_message"] = 'There is no active channel with session id.'
            response['message'] = 'There is no active channel with session id.'
            response["data"] = Channel_ids
            response["statuscode"] = 400
          
        logs["data"]["status_message"] = "Chat session listed successfully."
        response["data"] = Channel_ids
        response['message'] = 'Chat session listed successfully.'
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
