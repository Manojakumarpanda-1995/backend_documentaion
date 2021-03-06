from usermanagement.models import Users, AccessManagement, Roles
from usermanagement.utils.hash import encryption,decryption
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
import datetime

from organization.models import UserCompanyRole
from project.models import ProjectUsers


actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_list_users_by_project(request_data, token):
	try:
		response={}

		logs = {
			"Client_IP_Address": request_data["Client_IP_Address"],
			"Remote_ADDR": request_data["Remote_ADDR"],
			"data": {
				"Requested_URL": request_data["Requested_URL"]
			},
			"ProjectID": request_data["project_id"]
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
		isAuthorized = True
		
		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company_id"]:
				apiParamsInfo[key] = value

		if isAuthorized:
			data = []
			getProjectUsers = ProjectUsers.objects.filter(project__project_id=apiParamsInfo["project_id"], isActive=True, user__isActive=True)

			if len(getProjectUsers) > 0:
				isAlreadyAdded = []
				data = []
				getCompanyAdmin = UserCompanyRole.objects.filter(role__role_name="COMPANY-ADMIN", isActive=True, company=getProjectUsers[0].user.company)
				for companyAdmin in getCompanyAdmin:
					if companyAdmin.user.id not in isAlreadyAdded:
						isAlreadyAdded.append(companyAdmin.user.id)
						data.append({
							"name": companyAdmin.user.name,
							"role": companyAdmin.role.role_name
						})
				
				for projectUser in getProjectUsers:
					if projectUser.user.user.id not in isAlreadyAdded:
						isAlreadyAdded.append(projectUser.user.user.id)
						data.append({
							"name": projectUser.user.user.name,
							"role": projectUser.user.role.role_name
						})
				logs["data"]["status_message"] = "Users listed successfully."

				response["data"] = data
				response['message'] = "Users listed successfully."
				response["statuscode"] = 200
			else:
				logs["data"]["status_message"] = "No users found corresponding to the project."

				response['message'] = "No users found corresponding to the project."
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