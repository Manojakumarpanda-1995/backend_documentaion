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

from organization.models import UserCompanyRole
from project.models import ProjectInfo, ProjectUsers

secret = getattr(settings, "SECRET_KEY", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_assign_project(request_data, token):
	try:
		response={}
		
		logs = {
			"Client_IP_Address": request_data["Client_IP_Address"],
			"Remote_ADDR": request_data["Remote_ADDR"],
			"data": {
				"Requested_URL": request_data["Requested_URL"]
			},
			"Project": request_data["project"]
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
																# company__id=request_data["company_id"],
																company__active=True, 
																role__active=True, 
																isActive=True)

		# Get all roles
		isAuthorized = False
		isUserCompanyRole = False
		allRoles = []
		for user in getUserCompanyRole:
			if user.role.role_name.upper() not in allRoles:
				allRoles.append(user.role.role_name.upper())

		if "SUPER-USER" in allRoles:
			isAuthorized = True
			getUserCompanyRole = UserCompanyRole.objects.filter(id=request_data["user"])

			if len(getUserCompanyRole) > 0:
				getUserCompanyRole = getUserCompanyRole[0]
				if not getUserCompanyRole.user.active:
					logs["data"]["data_fields"] = [request_data["client_id"], apiParamsInfo["project"]]
					logs["data"]["status_message"] = "User is not active."

					response['message'] = "User is not active."
					response["statuscode"] = 400
					return response

				elif not getUserCompanyRole.company.active:
					logs["data"]["data_fields"] = [request_data["client_id"], apiParamsInfo["project"]]
					logs["data"]["status_message"] = "Company is not active."

					response['message'] = "Company is not active."
					response["statuscode"] = 400
					return response

				elif not getUserCompanyRole.role.active:
					logs["data"]["data_fields"] = [request_data["client_id"], apiParamsInfo["project"]]
					logs["data"]["status_message"] = "Role is not active."

					response['message'] = "Role is not active."
					response["statuscode"] = 400
					return response

				elif not getUserCompanyRole.isActive:
					logs["data"]["data_fields"] = [request_data["client_id"], apiParamsInfo["project"]]
					logs["data"]["status_message"] = "UserCompanyRole is not active."

					response['message'] = "UserCompanyRole is not active."
					response["statuscode"] = 400
					return response

				if getUserCompanyRole.role.role_name in ["COMPANY-ADMIN", "PROJECT-ADMIN", "USER"]:
					isUserCompanyRole = True
		elif "COMPANY-ADMIN" in allRoles:
			getUserCompanyRole = UserCompanyRole.objects.filter(id=request_data["user"])

			if len(getUserCompanyRole) > 0:
				getUserCompanyRole = getUserCompanyRole[0]
				if not getUserCompanyRole.user.active:
					logs["data"]["data_fields"] = [request_data["client_id"], apiParamsInfo["project"]]
					logs["data"]["status_message"] = "User is not active."

					response['message'] = "User is not active."
					response["statuscode"] = 400
					return response

				elif not getUserCompanyRole.company.active:
					logs["data"]["data_fields"] = [request_data["client_id"], apiParamsInfo["project"]]
					logs["data"]["status_message"] = "Company is not active."

					response['message'] = "Company is not active."
					response["statuscode"] = 400
					return response

				elif not getUserCompanyRole.role.active:
					logs["data"]["data_fields"] = [request_data["client_id"], apiParamsInfo["project"]]
					logs["data"]["status_message"] = "Role is not active."

					response['message'] = "Role is not active."
					response["statuscode"] = 400
					return response

				elif not getUserCompanyRole.isActive:
					logs["data"]["data_fields"] = [request_data["client_id"], apiParamsInfo["project"]]
					logs["data"]["status_message"] = "UserCompanyRole is not active."

					response['message'] = "UserCompanyRole is not active."
					response["statuscode"] = 400
					return response

				if getUserCompanyRole.role.role_name in ["PROJECT-ADMIN", "USER"]:
					isUserCompanyRole = True
			isAuthorized = True
		else:
			logs["data"]["status_message"] = 'You are not authorized to assign project.'
			response['message'] = 'You are not authorized to assign project.'
			response["statuscode"] = 400
			return response


		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company_id", "client_id"]:
				apiParamsInfo[key] = value

		if isAuthorized:
			if isUserCompanyRole:
				apiParamsInfo["user"] = getUserCompanyRole
				getProject = ProjectInfo.objects.filter(id=apiParamsInfo["project"])
				# getModule = ProjectModules.objects.filter(id=apiParamsInfo["module"])

				if len(getProject) > 0:
					apiParamsInfo["project"] = getProject[0]
					getProjectUsers = ProjectUsers.objects.filter(project=apiParamsInfo["project"], project__isActive=True)
					
					if len(getProjectUsers) > 0:
						getProjectUsers = getProjectUsers[0]
						if getProjectUsers.user.company.id != apiParamsInfo["user"].company.id:
							logs["data"]["data_fields"] = [apiParamsInfo["project"].id]
							logs["data"]["status_message"] = "Project and User have different companies."

							response['message'] = "Project and User have different companies."
							response["statuscode"] = 400
							actvity_logs.insert_one(logs)
							return response


					getUserProject = ProjectUsers.objects.filter(user=apiParamsInfo["user"], project=apiParamsInfo["project"], project__isActive=True)

					if len(getUserProject) == 0:
						apiParamsInfo["created_by"] = curr_user
						apiParamsInfo["updated_by"] = apiParamsInfo["created_by"]

						getUserProject = ProjectUsers.objects.create(**apiParamsInfo)

						logs["data"]["data_fields"] = [getUserCompanyRole.user.name, getUserCompanyRole.company.name, getProject[0].name]
						logs["data"]["status_message"] = "Project assigned successfully."

						response["data"] = getUserProject.id
						response['message'] = 'Project assigned successfully.'
						response["statuscode"] = 200
					else:
						logs["data"]["data_fields"] = [getUserCompanyRole.user.name, getUserCompanyRole.company.name, getProject[0].name]
						logs["data"]["status_message"] = "Project already assigned."

						response['message'] = 'Project already assigned.'
						response["statuscode"] = 400
					# else:
					# 	logs["data"]["data_fields"] = [apiParamsInfo["module_id"]]
					# 	logs["data"]["status_message"] = "Module with given ID doesn't exist."

					# 	response['message'] = "Module with given ID doesn't exist."
					# 	response["statuscode"] = 400

				else:
					logs["data"]["data_fields"] = [request_data["client_id"], apiParamsInfo["project"]]
					logs["data"]["status_message"] = "Project with given ID doesn't exist."

					response['message'] = "Project with given ID doesn't exist."
					response["statuscode"] = 400
			else:
				logs["data"]["data_fields"] = [request_data["client_id"], apiParamsInfo["project"]]
				logs["data"]["status_message"] = "User is not the part of company provided."

				response['message'] = "User is not the part of company provided."
				response["statuscode"] = 400
		else:
			logs["data"]["data_fields"] = [request_data["client_id"], apiParamsInfo["project"]]
			logs["data"]["status_message"] = 'Only SuperUser or Company-Admin can assign the projects.'
			response['message'] = 'Only SuperUser or Company-Admin can assign the projects.'
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