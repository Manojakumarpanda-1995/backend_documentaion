# import uuid
# import hashlib
import datetime
import logging
# import re
import os
import sys

from rest_framework.response import Response
from django.conf import settings
from django.http import FileResponse
from django.utils import timezone
from usermanagement.models import (  # AccessManagement, Roles,TemporaryURL
    TemporaryURL, Users)
# from usermanagement.utils.hash import (decryption, encryption,
#                                        removeSpecialCharacters)

media_file = getattr(settings, "MEDIA_ROOT", None)
secret = getattr(settings, "SECRET_KEY", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_download_file(request_data, token):
    try:
        response = {}
        request_data["download_token"] = request_data["uid"]
        # Unpack list value
        for key in request_data:
            if type(request_data[key]) == list:
                request_data[key] = request_data[key][0]
        logs = {
            "Client_IP_Address": request_data["Client_IP_Address"],
            "Remote_ADDR": request_data["Remote_ADDR"],
            "data": {
                "Requested_URL": request_data["Requested_URL"]
            },
            "DownloadToken": request_data["download_token"]
        }

        curr_user = Users.objects.filter(token=token)
        if len(curr_user) == 0:
            logs["data"]["status_message"] = "Invalid Token."
            response['message'] = "Invalid Token."
            response["statuscode"] = 400

            actvity_logs.insert_one(logs)
            return Response(response)
        else:
            curr_user = curr_user[0]
            logs["User"] = curr_user.id

        # logging.info(str(request_data))
        apiParamsInfo = {}
        for key, value in request_data.items():
            if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company_id", "client_id"]:
                apiParamsInfo[key] = value

        getDownload = TemporaryURL.objects.get(token=apiParamsInfo["download_token"])
        logs["data"]["data_fields"] = [apiParamsInfo["download_token"]]

        if (getDownload.expiry_time is not None) and (getDownload.expiry_time >= timezone.now()):
            filepath = getDownload.filepath
            filename = getDownload.filename
            getDownload.delete()
            # wrapper = FileWrapper(open(filepath,"rb"))
            # if filepath.split(".")[-1]  in ["xlsx","xlsb"]:
            #     response = HttpResponse(wrapper, content_type='application/vnd.ms-excel')
            # response['Content-Disposition'] = 'attachment; filename=%s' % filename
            # response['Content-Length'] = os.path.getsize(filepath)
            logs["added_at"] = datetime.datetime.utcnow()
            actvity_logs.insert_one(logs)

            return FileResponse(open(filepath, "rb"))
        else:
            getDownload.delete()
            response = {}
            response["statuscode"] = 400
            response["message"] = "URL Expired"
            logs["added_at"] = datetime.datetime.utcnow()
            actvity_logs.insert_one(logs)
            return Response(response)
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
        return Response(response)
