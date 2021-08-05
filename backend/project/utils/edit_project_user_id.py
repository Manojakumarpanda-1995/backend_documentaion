from usermanagement.models import Users, AccessManagement, Roles
from usermanagement.utils.hash import encryption, decryption
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
import datetime
import uuid
import shutil

from organization.models import UserCompanyRole
from project.models import ProjectUsers

actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_edit_project_user_id(request_data, token):
	try:
		response={}

		# Unpack list value
		# for key in request_data:
		# 	if type(request_data[key]) == list:
		# 		request_data[key] = request_data[key][0]
		
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


		# Get all roles
		# Get UserCompanyRole
			getUserCompanyRole = UserCompanyRole.objects.filter(user=curr_user, 
																user__active=True,
																# company__id=request_data["company_id"],
																company__active=True, 
																role__active=True, 
																isActive=True)

		# Get all roles
		isAuthorized = False
		displayData = []
		allRoles = []
		for user in getUserCompanyRole:
			if user.role.role_name.upper() not in allRoles:
				allRoles.append(user.role.role_name.upper())
		if "SUPER-USER" in allRoles:
			isAuthorized = True
		if "PROJECT-ADMIN" in allRoles:
			isAuthorized = True
		if "COMPANY-ADMIN" in allRoles:
			isAuthorized = True
		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company_id"]:
				apiParamsInfo[key] = value

		changed_values = []

		if isAuthorized:
			getProjectUser = ProjectUsers.objects.filter(id=apiParamsInfo["project_user_id"])

			if len(getProjectUser) > 0:
				getProjectUser = getProjectUser[0]

				name_list = []

				for key in apiParamsInfo:
					if key == "user_first_name":
						changed_values.append([getProjectUser.user.user.first_name,  apiParamsInfo["user_first_name"]])
						getProjectUser.user.user.first_name = apiParamsInfo["user_first_name"]
						getProjectUser.user.user.save()
						name_list.append(apiParamsInfo["user_first_name"])
					elif key == "user_last_name":
						changed_values.append([getProjectUser.user.user.last_name,  apiParamsInfo["user_last_name"]])
						getProjectUser.user.user.last_name = apiParamsInfo["user_last_name"]
						getProjectUser.user.user.save()
						name_list.append(apiParamsInfo["user_last_name"])
					elif key == "user_email":
						changed_values.append([getProjectUser.user.user.email,  apiParamsInfo["user_email"]])
						getProjectUser.user.user.email = apiParamsInfo["user_email"]
						getProjectUser.user.user.save()
					elif key == "user_role":
						getRole = Roles.objects.get(id=apiParamsInfo["user_role"])
						if "PROJECT-ADMIN" in allRoles and getRole.role_name=="PROJECT-ADMIN":
							logging.info('Users11==>{}'.format(getRole.role_name))
							logs["data"]["data_fields"] = [apiParamsInfo["project_user_id"], changed_values]
							logs["data"]["status_message"] = "You are not authorized to edit project details."

							response['message'] = "You are not authorized to edit project details."
							response["statuscode"] = 400
							return response
						changed_values.append([getProjectUser.user.role.role_name,  apiParamsInfo["user_role"]])
						if (getRole.role_name != "PROJECT-ADMIN") and (getProjectUser.user.role.role_name == "PROJECT-ADMIN") and (getProjectUser.isActive):
							getActiveProjectUsers = ProjectUsers.objects.filter(project = getProjectUser.project, user__role__role_name="PROJECT-ADMIN", isActive=True)

							if len(getActiveProjectUsers) < 2:
								logs["data"]["data_fields"] = [apiParamsInfo["project_user_id"]]
								logs["data"]["status_message"] = "Project should have atleast one project admin."

								response['message'] = "Project should have atleast one project admin."
								response["statuscode"] = 400
								return response

						getProjectUser.user.role = getRole
						getProjectUser.user.save()
					elif key == "user_expiry_date":
						changed_values.append([getProjectUser.expiry_date,  apiParamsInfo["user_expiry_date"]])
						getProjectUser.expiry_date = datetime.datetime.strptime(apiParamsInfo["user_expiry_date"], "%Y-%m-%d %H:%M")
						getProjectUser.save()
					elif key == "user_status":
						if (not apiParamsInfo["user_status"]) and (getProjectUser.user.role.role_name == "PROJECT-ADMIN") and (getProjectUser.isActive):
							getActiveProjectUsers = ProjectUsers.objects.filter(project = getProjectUser.project, user__role__role_name="PROJECT-ADMIN", isActive=True)

							if len(getActiveProjectUsers) < 2:
								logs["data"]["data_fields"] = [apiParamsInfo["project_user_id"]]
								logs["data"]["status_message"] = "Project should have atleast one project admin."

								response['message'] = "Project should have atleast one project admin."
								response["statuscode"] = 400
								return response

						changed_values.append([getProjectUser.isActive,  apiParamsInfo["user_status"]])
						getProjectUser.isActive = apiParamsInfo["user_status"]
						getProjectUser.save()
				
				if len(name_list) > 0:
					getProjectUser.user.user.name = " ".join([i.strip() for i in name_list])
					# getProjectUser.user.user.save()


				logs["data"]["data_fields"] = [apiParamsInfo["project_user_id"], changed_values]
				logs["data"]["status_message"] = "Project data updated successfully."

				logs["Project"] = getProjectUser.project.project_id

				response['message'] = "Project data updated successfully."
				response["statuscode"] = 200
			
			else:
				logs["data"]["data_fields"] = [apiParamsInfo["project_user_id"], changed_values]
				logs["data"]["status_message"] = "Project User with provided ID doesn't exist."

				response['message'] = "Project User with provided ID doesn't exist."
				response["statuscode"] = 400
		else:
			logs["data"]["data_fields"] = [apiParamsInfo["project_user_id"], changed_values]
			logs["data"]["status_message"] = "You are not authorized to edit project details."

			response['message'] = "You are not authorized to edit project details."
			response["statuscode"] = 400

		logs["added_at"] = datetime.datetime.utcnow()
		actvity_logs.insert_one(logs)
		return response

	except Exception as e:
		response = {}
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