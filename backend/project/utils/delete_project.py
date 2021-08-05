from usermanagement.models import Users, AccessManagement, Roles
from usermanagement.utils.hash import encryption, decryption
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
import datetime

from organization.models import UserCompanyRole
from project.models import ProjectUsers, ProjectInfo

actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_deactivate_project(request_data, token):
	try:
		response={}
		
		logs = {
			"Client_IP_Address": request_data["Client_IP_Address"],
			"Remote_ADDR": request_data["Remote_ADDR"],
			"data": {
				"Requested_URL": request_data["Requested_URL"]
			},
			"Project": request_data["project_id"]
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
		isAuthorized = False
		getProject = None
		allRoles = []
		for user in getUserCompanyRole:
			if user.role.role_name.upper() not in allRoles:
				allRoles.append(user.role.role_name.upper())

		if "SUPER-USER" in allRoles:
			isAuthorized = True
		elif "COMPANY-ADMIN" in allRoles:
			isAuthorized = True
		
		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company_id"]:
				apiParamsInfo[key] = value

		changed_values = []

		if isAuthorized:
			# getProjectUsers = ProjectUsers.objects.filter(project__id=apiParamsInfo["project_id"])
			getProjectUsers = ProjectInfo.objects.filter(id=apiParamsInfo["project_id"])

			if len(getProjectUsers) > 0:
				for getProject in getProjectUsers:
					getProject.isActive = apiParamsInfo["status"]
					getProject.save()

				logs["data"]["data_fields"] = [apiParamsInfo["project_id"]]
				logs["data"]["status_message"] = "Project deactivated successfully."

				response['message'] = "Project deactivated successfully."
				response["statuscode"] = 200
			
			else:
				logs["data"]["data_fields"] = [apiParamsInfo["project_id"]]
				logs["data"]["status_message"] = "Project with provided ID doesn't exist."

				response['message'] = "Project with provided ID doesn't exist."
				response["statuscode"] = 400
		else:
			logs["data"]["data_fields"] = [apiParamsInfo["project_id"]]
			logs["data"]["status_message"] = "You are not authorized to deactivate project."

			response['message'] = "You are not authorized to deactivate project."
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