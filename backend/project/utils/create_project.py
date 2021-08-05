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
import shutil

from organization.models import UserCompanyRole, Company
from project.models import ProjectInfo

secret = getattr(settings, "SECRET_KEY", None)
media_files = getattr(settings, "MEDIA_ROOT", None)
static_files = getattr(settings, "STATIC_ROOT", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)



def func_create_project(request_data, token):
	try:
		response={}

		# Unpack list value
		for key in request_data:
			if type(request_data[key]) == list:
				request_data[key] = request_data[key][0]
		
		logs = {
			"Client_IP_Address": request_data["Client_IP_Address"],
			"Remote_ADDR": request_data["Remote_ADDR"],
			"data": {
				"Requested_URL": request_data["Requested_URL"]
			},
			"ProjectName": request_data["name"]
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
		allRoles = []
		for user in getUserCompanyRole:
			if user.role.role_name.upper() not in allRoles:
				allRoles.append(user.role.role_name.upper())

		if "SUPER-USER" in allRoles:
			isAuthorized = True
			getComapny = Company.objects.get(id=request_data["client_id"])
		elif "COMPANY-ADMIN" in allRoles:
			isAuthorized = True
			getComapny = Company.objects.get(id=request_data["company_id"])
		else:
			logs["data"]["status_message"] = 'You are not authorized to create project.'
			response['message'] = 'You are not authorized to create project.'
			response["statuscode"] = 400


		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company_id", "client_id"]:
				apiParamsInfo[key] = value

		if isAuthorized:
			project_name_hash = hashlib.sha256(" ".join([removeSpecialCharacters(getComapny.name + apiParamsInfo["name"]), secret]).encode()).hexdigest()

			getProject = ProjectInfo.objects.filter(project_name_hash=project_name_hash)

			if len(getProject) == 0:
				apiParamsInfo["project_name_hash"] = project_name_hash
				apiParamsInfo["project_id"] = uuid.uuid4().hex
			
				apiParamsInfo["created_by"] = curr_user
				apiParamsInfo["updated_by"] = apiParamsInfo["created_by"]

				getProject = ProjectInfo.objects.create(**apiParamsInfo)

				logs["data"]["data_fields"] = [apiParamsInfo["project_id"]]
				logs["data"]["status_message"] = "Project created successfully."

				response["data"] = getProject.id
				response['message'] = 'Project created successfully.'
				response["statuscode"] = 200

			else:
				logs["data"]["data_fields"] = [apiParamsInfo["name"]]
				logs["data"]["status_message"] = "Project already existed."

				response['message'] = "Project already existed."
				response["statuscode"] = 400
		else:
			logs["data"]["status_message"] = 'Only SuperUser or Company-Admin can create the projects.'
			response['message'] = 'Only SuperUser or Company-Admin can create the projects.'
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