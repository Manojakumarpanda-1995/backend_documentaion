from usermanagement.models import Users, AccessManagement, Roles
from usermanagement.utils.hash import encryption, decryption,generate_passwords,random_alphaNumeric_string
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
from django.utils import timezone
import datetime
import uuid
import re
from usermanagement.models import Users, AccessManagement,Workers
from usermanagement.tasks import send_email

from organization.models import UserCompanyRole

verify_link_exp = getattr(settings, "VERIFICATION_LINK_EXPIRY_DURATION", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)

#To validate email in the format of foo./_/+/123@some.com 
# 0->invalid,1->valid
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

def generate_hash():
	return uuid.uuid4().hex

def func_register_worker(request_data):
	try:
		response={}
		
		logs = {
			"Client_IP_Address": request_data["Client_IP_Address"],
			"Remote_ADDR": request_data["Remote_ADDR"],
			"data": {
				"Requested_URL": request_data["Requested_URL"]
			}
		}

		curr_user = Users.objects.filter(email__iexact=request_data["email"])
		if len(curr_user) == 0:
			pass
		else:
			logs["data"]["status_message"] = "Users with this email id's already exists. Try an another email."
			response['message'] = "Users with this email id's already exists. Try an another email."

			logs["added_at"] = datetime.datetime.utcnow()
			actvity_logs.insert_one(logs)
			response["statuscode"] = 400
			curr_user = curr_user[0]
			logs["User"] = curr_user.id
			return response

		# Get all roles
		isAuthorized = True
		
		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL"]:
				apiParamsInfo[key] = value
		

		if isAuthorized:
			apiParamsInfo["email"] = apiParamsInfo["email"].lower()
			getValidated=validate_email(email=apiParamsInfo['email'])
			if getValidated==0:
				logs["data"]["status_message"] = "Please try to add valid email."
				response['message'] = "Please try to add valid email."
				response["statuscode"] = 400
				actvity_logs.insert_one(logs)
				return response
			 
			getName = 0 if request_data.get("name",None) is None else 1
			getWorker =Workers.objects.filter(email__iexact=apiParamsInfo["email"])

			if getName != 0 and len(getWorker)==0:
				getWorker = Workers.objects.create(**apiParamsInfo)

				emails=["rohit@viewooletters.in",
						"nitin@viewooletters.in"]
				#emails=["manojakumarpanda@momenttext.com"]
				emails.append(str(getWorker.email))
				message="You'r registration request with Email:{} accepted successfully.\n Our Team will contact you soon.".format(
																getWorker.email
															)

				#Celery
				# send_email.delay(str({"email": emails,
				# 						"subject": "New Registration",
				# 						# "template_name": "generate_passwords", 
				# 						"template_name": message,
				# 						# "variables": [decryption(apiParamsInfo['password'])],
				# 						"email_type": "plain"
				# 						}))

				# logging.info("emails==>{}".format(emails))
				logs["data"]["data_fields"] = [apiParamsInfo["name"], apiParamsInfo["email"]]
				logs["data"]["status_message"] = "Workers registered successfully."
				response["data"] = getWorker.id
				response['message'] = 'Workers registered successfully.'
				response["statuscode"] = 200

			else:
				if len(getWorker)==0:
					logs["data"]["status_message"] = "Workers name can't be left blank."
					response['message'] = "Workers name can't be left blank."
				else:
					logs["data"]["status_message"] = "Workers already registered."
					response['message'] = "Workers already registered."
				logs["data"]["data_fields"] = [apiParamsInfo["email"]]
				response["statuscode"] = 400
		else:
			logs["data"]["data_fields"] = [ apiParamsInfo["email"]]
			logs["data"]["status_message"] = 'You are not authorized to create workers.'
			response['message'] = 'You are not authorized to create workers.'
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