from usermanagement.models import Users, AccessManagement, Roles
from usermanagement.utils.hash import encryption,decryption
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


def func_deactivate_usercompanyrole(request_data, token):
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

			# Get UserCompanyRole
			getUserCompanyRole = UserCompanyRole.objects.filter(user=curr_user,
																user__active=True,
																company__id=request_data["company_id"],
																company__active=True,
																role__active=True,
																isActive=True)

		# Get all roles
		# Superuser will only be superuser.
		isAuthorized = False
		roleIn = []
		allRoles = []
		for user in getUserCompanyRole:
			if user.role.role_name.upper() not in allRoles:
				allRoles.append(user.role.role_name.upper())

		if "SUPER-USER".upper() in allRoles:
			isAuthorized = True
			roleIn = ["COMPANY-ADMIN", "PROJECT-ADMIN", "USER"]
		elif "COMPANY-ADMIN".upper() in allRoles:
			roleIn = ["PROJECT-ADMIN", "USER"]
			isAuthorized = True
		elif "PROJECT-ADMIN".upper() in allRoles:
			roleIn = ["USER"]
			isAuthorized = False
		
		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company_id"]:
				apiParamsInfo[key] = value

		if isAuthorized:
			isUser = False
			getUser = Users.objects.filter(id=apiParamsInfo["user"])
			if len(getUser) > 0:
				isUser = True
				getUser = getUser[0]
			else:
				logs["data"]["data_fields"] = [apiParamsInfo["user"]]
				logs["data"]["status_message"] = "User with the provided ID is not found in the database."
				response['message'] = "User with the provided ID is not found in the database."
				response["statuscode"] = 400
				return response

			isCompany = False
			getCompany = Company.objects.filter(id=apiParamsInfo["company"])
			if len(getCompany) > 0:
				isCompany = True
				getCompany = getCompany[0]
			else:
				logs["data"]["data_fields"] = [apiParamsInfo["company"]]
				logs["data"]["status_message"] = "Company with the provided ID is not found in the database."
				response['message'] = "Company with the provided ID is not found in the database."
				response["statuscode"] = 400
				return response
			

			isRole = False
			getRole = Roles.objects.filter(id=apiParamsInfo["role"])
			if len(getRole) > 0:
				getRole = getRole[0]
				if getRole.role_name in roleIn:
					isRole = True
			else:
				logs["data"]["data_fields"] = [apiParamsInfo["role"]]
				logs["data"]["status_message"] = "Role with the provided ID is not found in the database."
				response['message'] = "Role with the provided ID is not found in the database."
				response["statuscode"] = 400
				return response

			if isUser and isCompany and isRole:
				getUserCompanyRole = UserCompanyRole.objects.filter(user=getUser, company=getCompany, role=getRole)
				
				# if len(getUserCompanyRole) == 0:
				# 	getUserCompany = UserCompanyRole.objects.filter(user=getUser, company=getCompany)

				if len(getUserCompanyRole) > 0:
					getUserCompanyRole = getUserCompanyRole[0]
					getUserCompanyRole.isActive = False
					getUserCompanyRole.save()

					logs["data"]["data_fields"] = [getUser.name, getCompany.name, getRole.role_name]
					logs["data"]["status_message"] = "UserCompanyRole deactivate successfully."

					response["data"] = getUserCompanyRole.id
					response['message'] = "UserCompanyRole deactivate successfully."
					response["statuscode"] = 200
					
					# else:
					# 	getUserCompany = getUserCompany[0]

					# 	logs["data"]["data_fields"] = [getUser.name, getCompany.name, getRole.role_name]
					# 	logs["data"]["status_message"] = "User in same company has already a role."

					# 	response["data"] = getUserCompany.id
					# 	response['message'] = "User in same company has already a role."
					# 	response["statuscode"] = 200
				else:
					logs["data"]["data_fields"] = [getUser.name, getCompany.name, getRole.role_name]
					logs["data"]["status_message"] = "UserCompanyRole doesnot exists."

					response['message'] = "UserCompanyRole doesnot exists."
					response["statuscode"] = 400
		else:
			logs["data"]["status_message"] = 'You cannot create the UserCompanyRole.'
			response['message'] = 'You cannot create the UserCompanyRole.'
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