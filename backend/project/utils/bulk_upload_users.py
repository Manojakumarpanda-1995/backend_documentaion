from usermanagement.models import Users, AccessManagement, Roles
from usermanagement.utils.hash import encryption, decryption, removeSpecialCharacters
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
import uuid
import json
import hashlib
import datetime
import pandas as pd
import numpy as np

from project.models import FileUpload, GetProgress
from project.tasks import bulkUploadUsers
from organization.models import *

media_files=getattr(settings,"MEDIA_ROOT")
secret = getattr(settings, "SECRET_KEY", None)
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
			logging.info('Matchs==>{}'.format(match))
			# match=re.findall(regex,email)
			return 1 if match else 0
	except Exception as e:
		pass

def func_bulk_user_upload(request_data, token):
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

		# logging.info('request_data==>{}'.format(request_data['client_id']))
		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company_id", "client_id"]:
				apiParamsInfo[key] = value

		apiParamsInfo["file"] = apiParamsInfo["file"][0]
		apiParamsInfo["project_id"] = apiParamsInfo["project_id"][0]

		curr_file = FileUpload.objects.create(original_file_name=str(apiParamsInfo["file"]), 
												datafile=apiParamsInfo["file"], 
												function_type="USER BULK UPLOAD",
												created_by=curr_user)
		try:
			#added by manoj
			df = pd.read_excel(io=os.path.join(media_files, str(curr_file.datafile)))
			df.rename(columns={
			"User Email": "user_email",
				"First Name": "first_name",
				"Last Name": "last_name",
				"Expiry Date (DD-MM-YYYY)": "expiry_date",
				"Expiry Time (HH:MM)": "expiry_time",},inplace=True)
			df = df.replace({np.nan: None})

			for row in df.itertuples():  
				# logging.info('ROws==>{}'.format(row))
				if row.user_email is not None:
					#This is to validate the users email format is correct or not.
					
					getValidated=validate_email(email=row.user_email)
					# logging.info("Validated==>{}".format(getValidated))
					if getValidated==0:
						logs["data"]["status_message"] = "Please try to add valid emails."
						response['message'] = "Please try to add valid emails."
						response["statuscode"] = 400
						actvity_logs.insert_one(logs)
						return response
					getUser = Users.objects.filter(email=row.user_email)
					if len(getUser):
						getUser=getUser[0]
						getSuperuser=UserCompanyRole.objects.filter(user=getUser,role__role_name="SUPER-USER")
						getUserCompanyRole=UserCompanyRole.objects.filter(user=getUser
																		,company__id__in=request_data['client_id']
																		,role__id__in=[2,3])
						#This is to check if the company admin or superusers email address in the file
						if len(getSuperuser) or len(getUserCompanyRole):
							response["message"] = "SUPER-USER OR COMPANY-ADMIN can't made as USER."
							response["statuscode"] = 400
							logs["data"]["status_message"] ="SUPER-USER OR COMPANY-ADMIN can't made as USER."
							logs["data"]['file'] = curr_file.id
							logs["added_at"] = datetime.datetime.utcnow()
							actvity_logs.insert_one(logs)
							return response
					else:
						pass
				else:
					pass
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			logging.info(str(exc_type) + " " + str(fname) + " " + str(exc_tb.tb_lineno) + " " + str(e))
			logs["data"]["data_fields"] = "You are trying to upload wrong files. "
			response["message"] = "You are trying to upload wrong files. "
			error_logs.insert_one(logs)
			response["statuscode"] = 400
			return response
			
		getGraph.bulk_user_upload = json.dumps({"message": "Uploading...", "isUploading": True, "refreshedTime": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")})
		getGraph.save()

		# Celery Task
		bulkUploadUsers.delay(str({"original_name": str(curr_file.original_file_name),
									"file": str(curr_file.datafile),
									"user_email": str(curr_user.email),
									"sheet_name": 0,
									"project_id": apiParamsInfo["project_id"]}))

		logs["data"]["data_fields"] = [str(curr_file.datafile)]

		response["message"] = "File uploaded successfully."
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