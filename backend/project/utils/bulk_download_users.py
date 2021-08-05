from usermanagement.models import Users, AccessManagement, Roles
from usermanagement.utils.hash import encryption, decryption, removeSpecialCharacters
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
import json
import uuid
import hashlib
import datetime

from organization.models import UserCompanyRole
from project.models import FileUpload, GetProgress, ProjectUsers
from project.tasks import bulkDownloadUsers

secret = getattr(settings, "SECRET_KEY", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_bulk_user_download(request_data, token):
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

			# Get UserCompanyRole
			getUserCompanyRole = UserCompanyRole.objects.filter(user=curr_user, 
																user__active=True,
																company=request_data["company_id"],
																company__active=True, 
																role__active=True, 
																isActive=True)

		# Get all roles
		isAuthorized = False
		role = None
		allRoles = []
		for user in getUserCompanyRole:
			if user.role.role_name.upper() not in allRoles:
				allRoles.append(user.role.role_name.upper())

		if "SUPER-USER" in allRoles:
			role = "SUPER-USER"
		elif "COMPANY-ADMIN" in allRoles:
			role = "COMPANY-ADMIN"
			userRoles = []
			
			# Get Role
			getProjectUsers = ProjectUsers.objects.filter(project__project_id=request_data["project_id"])

			# Check for Company Admin
			getUserCompanyRole = UserCompanyRole.objects.filter(company=getProjectUsers[0].user.company, user=curr_user, role__role_name="COMPANY-ADMIN", isActive=True)
			userRoles = []
			for user in getUserCompanyRole:
				if user.role.role_name.upper() not in userRoles:
					userRoles.append(user.role.role_name.upper())

			getProjectUsers = ProjectUsers.objects.filter(project__project_id=request_data["project_id"], user__user=curr_user, isActive=True, user__isActive=True)
			for user in getProjectUsers:
				if user.user.role.role_name.upper() not in userRoles:
					userRoles.append(user.user.role.role_name.upper())

			if "SUPER-USER" in userRoles:
				role = "SUPER-USER"
			elif "COMPANY-ADMIN" in userRoles:
				role = "COMPANY-ADMIN"
			elif "PROJECT-ADMIN" in userRoles:
				role = "PROJECT-ADMIN"
			else:
				role = "USER"
	
		elif "PROJECT-ADMIN" in allRoles:
			role = "PROJECT-ADMIN"

			# Get Role
			getProjectUsers = ProjectUsers.objects.filter(project__project_id=request_data["project_id"])

			# Check for Company Admin
			getUserCompanyRole = UserCompanyRole.objects.filter(company=getProjectUsers[0].user.company, user=curr_user, role__role_name="COMPANY-ADMIN", isActive=True)
			userRoles = []
			for user in getUserCompanyRole:
				if user.role.role_name.upper() not in userRoles:
					userRoles.append(user.role.role_name.upper())

			getProjectUsers = ProjectUsers.objects.filter(project__project_id=request_data["project_id"], user__user=curr_user, isActive=True, user__isActive=True)
			for user in getProjectUsers:
				if user.user.role.role_name.upper() not in userRoles:
					userRoles.append(user.user.role.role_name.upper())

			if "SUPER-USER" in userRoles:
				role = "SUPER-USER"
			elif "COMPANY-ADMIN" in userRoles:
				role = "COMPANY-ADMIN"
			elif "PROJECT-ADMIN" in userRoles:
				role = "PROJECT-ADMIN"
			else:
				role = "USER"
		else:
			logs["data"]["status_message"] = 'You are not authorized to create project user.'
			response['message'] = 'You are not authorized to create project.'
			response["statuscode"] = 400

		getGraph = GetProgress.objects.filter(user=curr_user)
		if len(getGraph) == 0:
			getGraph = GetProgress.objects.create(user=curr_user)
		else:
			getGraph = getGraph[0]


		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company_id", "client_id"]:
				apiParamsInfo[key] = value
		
		getGraph.bulk_user_download = json.dumps({"message": "Creating File...", "isDownloading": True, "refreshedTime": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")})
		getGraph.save()


		# Celery Task
		bulkDownloadUsers.delay(str({"project_id": apiParamsInfo["project_id"],
									"user_email": str(curr_user.email),
									"role": role}))

		logs["data"]["data_fields"] = [apiParamsInfo["project_id"]]

		response["message"] = "File downloaded successfully."
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