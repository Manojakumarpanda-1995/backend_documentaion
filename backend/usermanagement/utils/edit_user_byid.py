from usermanagement.models import Users, AccessManagement, Roles
from usermanagement.utils.hash import encryption, decryption
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
import datetime

actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)

#To validate email in the format of foo./_/+/123@some.com 
#0->invalid,1->valid
def validate_email(email):
	try:
		if (re.search("[!#$%^&*()?=,<>/]",email)):
			return 0
		else:
			regex='[A-Z0-9a-z._+-]+[@][a-z]+[.]+[a-z]{2,3}'
			match=re.match(regex,email)
			# match=re.findall(regex,email)
			return 1 if match else 0
	except Exception as e:
		pass

def func_edit_user_byid(request_data, token):
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

		
		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL"]:
				apiParamsInfo[key] = value


		getUser = Users.objects.get(id=apiParamsInfo["user_id"])
		if "email" in apiParamsInfo.keys():
			getValidated=validate_email(email=apiParamsInfo["email"])
			if getValidated==0:
				logs["data"]["status_message"] = "Pleasetry to  add valid email."
				response['message'] = "Please try to add valid email."
				response["statuscode"] = 400
				actvity_logs.insert_one(logs)
				return response
		changed_values = []
		for key, value in apiParamsInfo.items():
			if key in [f.name for f in getUser._meta.get_fields()]:
				changed_values.append((getattr(getUser, key), apiParamsInfo[key]))
				setattr(getUser, key, apiParamsInfo[key])

		getUser.save()

		logs["data"]["data_fields"] = [changed_values]
		logs["data"]["status_message"] = "User data updated successfully."

		response['message'] = "User data updated successfully."
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