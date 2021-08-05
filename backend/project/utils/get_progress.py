from usermanagement.models import Users, AccessManagement, Roles
from usermanagement.utils.hash import encryption, decryption, removeSpecialCharacters
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
import uuid
import hashlib
import datetime
import ast
import json

from project.models import FileUpload, GetProgress
from project.tasks import bulkDownloadUsers

secret = getattr(settings, "SECRET_KEY", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_get_progress(request_data, token):
	try:
		response={}
		
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

		getGraph = GetProgress.objects.filter(user=curr_user)
		if len(getGraph) == 0:
			getGraph = GetProgress.objects.create(user=curr_user)
		else:
			getGraph = getGraph[0]


		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company_id", "client_id"]:
				apiParamsInfo[key] = value
		
		if apiParamsInfo["progress_type"] == "BULK-UPLOAD":
			logging.info(str(getGraph.bulk_user_upload))
			# response["data"] = ast.literal_eval(getGraph.bulk_user_upload)
			response["data"] = json.loads(getGraph.bulk_user_upload)
		elif apiParamsInfo["progress_type"] == "BULK-DOWNLOAD":
			# response["data"] = ast.literal_eval(getGraph.bulk_user_download)
			response["data"] = json.loads(getGraph.bulk_user_download)
		elif apiParamsInfo["progress_type"] == "PROJECT-USER-LOGS":
			response["data"] = json.loads(getGraph.get_user_logs)
		elif apiParamsInfo["progress_type"] == "BASE-FILE-UPLOAD":
			response["data"] = json.loads(getGraph.base_file_upload)			

		logs["data"]["data_fields"] = [apiParamsInfo["progress_type"]]

		response["message"] = "File status retrieved successfully."
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