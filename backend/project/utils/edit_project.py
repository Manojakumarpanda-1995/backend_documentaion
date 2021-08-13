from usermanagement.models import Users, AccessManagement, Roles
from usermanagement.utils.hash import encryption, decryption, removeSpecialCharacters
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
import datetime
import uuid
import shutil
import hashlib

from organization.models import UserCompanyRole
from project.models import ProjectInfo, ProjectUsers

secret = getattr(settings, "SECRET_KEY", None)
media_files = getattr(settings, "MEDIA_ROOT", None)
static_files = getattr(settings, "STATIC_ROOT", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def storeLogoToStatic(file_name, old_file):
	full_file_name = os.path.join(media_files, file_name)
	if os.path.isfile(os.path.join(static_files, old_file)):
		os.remove(os.path.join(static_files, old_file))
	if os.path.isfile(full_file_name):
		newfile_name = os.path.basename(file_name)
		newfile_name = newfile_name.split(".")
		newfile_name = ".".join([str(uuid.uuid4().hex), newfile_name[1]])
		newfile_name = os.path.join(os.path.dirname(file_name), newfile_name)
		if not os.path.isdir(os.path.dirname(os.path.join(static_files, newfile_name))):
			os.makedirs(os.path.dirname(os.path.join(static_files, newfile_name)))
		shutil.copyfile(full_file_name, os.path.join(static_files, newfile_name))
		return newfile_name
	else:
		return None


def func_edit_project(request_data, token):
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
			getProject = ProjectInfo.objects.filter(id=apiParamsInfo["project"])

			if len(getProject) > 0:
				getProject = getProject[0]

				# Check if name is in keys
				if "name" in apiParamsInfo:
					getCompany = ProjectUsers.objects.filter(project__id=apiParamsInfo["project"])

					if len(getCompany) > 0:
						getCompany = getCompany[0].user.company
						project_name_hash = hashlib.sha256(" ".join([removeSpecialCharacters(getCompany.name + apiParamsInfo["name"]), secret]).encode()).hexdigest()
						getProjectHash = ProjectInfo.objects.filter(project_name_hash=project_name_hash)
						if (len(getProjectHash) > 0) and (getProjectHash[0].id != int(apiParamsInfo["project"])):
							logs["data"]["data_fields"] = [apiParamsInfo["project"], []]
							logs["data"]["status_message"] = "Project with the same name already exists."

							response['message'] = "Project with the same name already exists."
							response["statuscode"] = 400
							return response

				for key, value in apiParamsInfo.items():
					if key in [f.name for f in getProject._meta.get_fields()]:
						if key != "logo":
							changed_values.append((getattr(getProject, key), apiParamsInfo[key]))
						setattr(getProject, key, apiParamsInfo[key])

				getProject.save()

				if ("logo" in apiParamsInfo):
					old_logo = getProject.logo.name
					newfile_name = storeLogoToStatic(getProject.logo.name, old_logo)
					if newfile_name is not None:
						getProject.logo.name = newfile_name
						getProject.save()

				logs["data"]["data_fields"] = [apiParamsInfo["project"], changed_values]
				logs["data"]["status_message"] = "Project data updated successfully."

				response['message'] = "Project data updated successfully."
				response["statuscode"] = 200
			
			else:
				logs["data"]["data_fields"] = [apiParamsInfo["project"], changed_values]
				logs["data"]["status_message"] = "Project with provided ID doesn't exist."

				response['message'] = "Project with provided ID doesn't exist."
				response["statuscode"] = 400
		else:
			logs["data"]["data_fields"] = [apiParamsInfo["project"], changed_values]
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