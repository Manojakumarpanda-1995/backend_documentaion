from usermanagement.models import Users, AccessManagement, Roles
from usermanagement.utils.hash import encryption, decryption
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
from project.models import ProjectUsers

secret = getattr(settings, "SECRET_KEY", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_list_projects(request_data, token):
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
		isAuthorized = False
		displayData = []
		allRoles = []
		for user in getUserCompanyRole:
			if user.role.role_name.upper() not in allRoles:
				allRoles.append(user.role.role_name.upper())

		if "SUPER-USER" in allRoles:
			isAuthorized = True
			isEditable = True
			getProjects = ProjectUsers.objects.filter(user__company__id=request_data["client_id"])

			for project in getProjects:
				if isEditable:
					displayData.append({
						"id": project.project.id,
						"user_name": project.user.user.name,
						"user_email": project.user.user.email,
						"company_name": project.user.company.name,
						"role": project.user.role.role_name,
						"name": project.project.name,
						"project_id": project.project.project_id,
						"status": project.project.isActive,
						"created_at": project.project.created_at,
						"isEditable": isEditable
					})
		elif "COMPANY-ADMIN" in allRoles:
			isAuthorized = True
			getProjects = ProjectUsers.objects.filter(user__company__id=request_data["client_id"])

			for project in getProjects:
				getUserCompanyRole = UserCompanyRole.objects.filter(user=curr_user, 
																	user__active=True,
																	company=project.user.company,
																	company__active=True, 
																	role__active=True, 
																	isActive=True)
				allRoles = []
				for user in getUserCompanyRole:
					if user.role.role_name.upper() not in allRoles:
						allRoles.append(user.role.role_name.upper())

				isEditable = False

				if "SUPER-USER" in allRoles:
					isEditable = True
				elif "COMPANY-ADMIN" in allRoles:
					isEditable = True

				if (curr_user.id == project.user.user.id) and (project.user.role.role_name in ["PROJECT-ADMIN"]):
					isEditable = True


				if isEditable:
					displayData.append({
						"id": project.project.id,
						"user_name": project.user.user.name,
						"user_email": project.user.user.email,
						"company_name": project.user.company.name,
						"role": project.user.role.role_name,
						"created_at": project.project.created_at,
						"name": project.project.name,
						"project_id": project.project.project_id,
						"status": project.project.isActive,
						"isEditable": isEditable
					})
		elif "PROJECT-ADMIN" in allRoles:
			isAuthorized = True
			getProjects = ProjectUsers.objects.filter(user__user=curr_user, 
												user__company__id=request_data["client_id"], 
												project__isActive=True,
												isActive=True)

			for project in getProjects:
				isEditable = False
				
				if (curr_user.id == project.user.user.id) and (project.user.role.role_name in ["PROJECT-ADMIN"]):
					isEditable = True

				
				if isEditable:
					displayData.append({
						"id": project.project.id,
						"user_name": project.user.user.name,
						"user_email": project.user.user.email,
						"company_name": project.user.company.name,
						"role": project.user.role.role_name,
						"name": project.project.name,
						"project_id": project.project.project_id,
						"created_at": project.project.created_at,
						"status": project.project.isActive,
						"isEditable": isEditable
					})
		elif "USER" in allRoles:
			isAuthorized = True
			isEditable = False
			getProjects = ProjectUsers.objects.filter(user__user=curr_user, 
												user__company__id=request_data["client_id"], 
												project__isActive=True,
												user__isActive=True,
												isActive=True)

			for project in getProjects:

				if isEditable:
					displayData.append({
						"id": project.project.id,
						"user_name": project.user.user.name,
						"user_email": project.user.user.email,
						"company_name": project.user.company.name,
						"role": project.user.role.role_name,
						"name": project.project.name,
						"project_id": project.project.project_id,
						"created_at": project.project.created_at,
						"status": project.project.isActive,
						"isEditable": isEditable
					})
		else:
			logs["data"]["status_message"] = 'You are not authorized to list module.'
			response['message'] = 'You are not authorized to list module.'
			response["statuscode"] = 400


		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company_id", "client_id"]:
				apiParamsInfo[key] = value

		if isAuthorized:			
			logs["data"]["status_message"] = "Projects listed successfully."

			response["data"] = displayData
			response['message'] = 'Projects listed successfully.'
			response["statuscode"] = 200
		else:
			logs["data"]["status_message"] = 'You cannot list the projects.'
			response['message'] = 'You cannot list the projects.'
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