from usermanagement.models import Users, AccessManagement, Roles
from usermanagement.utils.hash import encryption,decryption
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
import datetime

from organization.models import UserCompanyRole, Company

actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_list_company_byemail(request_data, token):
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

			request_data["email"] = request_data["email"].lower()

			# Get UserCompanyRole
			getUserCompanyRole = UserCompanyRole.objects.filter(user__email=request_data["email"], 
																user__active=True,
																company__active=True, 
																role__active=True, 
																isActive=True)

		# Get all roles
		isAuthorized = True
		# displayData = None
		# for user in getUserCompanyRole:
		# 	if user.role.role_name.upper() in ["SUPER-USER"]:
		# 		isAuthorized = True
		# 		displayData = 'ALL'
		# 		break
		
		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company_id"]:
				apiParamsInfo[key] = value

		if isAuthorized:
			data = []
			companyAdded = []

			for company in getUserCompanyRole:
				if company.company.id not in companyAdded:
					companyAdded.append(company.company.id)

					allRoles = []
					getRoles = UserCompanyRole.objects.filter(user__email=request_data["email"],
																company=company.company,
																user__active=True,
																company__active=True, 
																role__active=True, 
																isActive=True).values("role__role_name")

					for role in getRoles:
						allRoles.append(role["role__role_name"])
					
					role = None

					if "SUPER-USER" in allRoles:
						role = "SUPER-USER"
					elif "COMPANY-ADMIN" in allRoles:
						role = "COMPANY-ADMIN"
					elif "PROJECT-ADMIN" in allRoles:
						role = "PROJECT-ADMIN"
					else:
						role = "USER"

					data.append({
						"id": company.company.id,
						"name": company.company.name,
						"role": role
					})

			logs["data"]["status_message"] = "List companies successfully."

			response["data"] = data
			response['message'] = "List companies successfully."
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