from usermanagement.models import Users, AccessManagement, Roles
from usermanagement.utils.hash import encryption,decryption
# from backend.encryptionAES import generateRandomKey
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
import datetime

from organization.models import Company, UserCompanyRole

actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_create_company(request_data, token):
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

			response["message"] = "Invalid Token."
			response["statuscode"] = 500

			actvity_logs.insert_one(logs)
			return response
		else:
			curr_user = curr_user[0]
			logs["User"] = curr_user.id

			# Get UserCompanyRole
			getUserCompanyRole = UserCompanyRole.objects.filter(user=curr_user,
																user__active=True,
																company__id=request_data["company_id"],
																company__active=True,
																role__active=True,
																isActive=True)

		# Get all roles
		isAuthorized = False
		allRoles = []
		for user in getUserCompanyRole:
			if user.role.role_name.upper() not in allRoles:
				allRoles.append(user.role.role_name.upper())
		
		if "SUPER-USER".upper() in allRoles:
			isAuthorized = True
		
		comapnyInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company_id"]:
				comapnyInfo[key] = value

		if isAuthorized:
			# Get Company Name
			getCompanyId = None
			spcl_company_name = re.sub('[^A-Za-z0-9\s]+', '', comapnyInfo["name"])
			getCompany = Company.objects.all().values("name", "id")
			
			for comp in getCompany:
				spcl_comp_name = re.sub('[^A-Za-z0-9\s]+', '', comp["name"])

				if spcl_company_name.upper() == spcl_comp_name.upper():
					getCompanyId = comp["id"]
					break
			
			if getCompanyId is None:
				comapnyInfo["created_by"] = curr_user
				comapnyInfo["updated_by"] = comapnyInfo["created_by"]

				getCompany = Company.objects.create(**comapnyInfo)

				response["data"] = getCompany.id
				logs["data"]["data_fields"] = [comapnyInfo["name"]]
				logs["data"]["status_message"] = "Company created successfully."

				response['message'] = 'Company created successfully.'
				response["statuscode"] = 200

			else:
				logs["data"]["data_fields"] = [comapnyInfo["name"]]
				logs["data"]["status_message"] = 'Company name already exists'
				response['message'] = 'Company name already exists'
				response["statuscode"] = 400
		else:
			logs["data"]["data_fields"] = [comapnyInfo["name"]]
			logs["data"]["status_message"] = 'Only Super User can create a company.'
			response['message'] = 'Only Super User can create a company.'
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