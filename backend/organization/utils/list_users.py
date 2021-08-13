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


def func_list_users(request_data, token):
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

		
		userCompanyRoleIDs = []
		freeUsers = []
		# Get Free Users
		getUserCompanyRole = UserCompanyRole.objects.all()
		for usr in getUserCompanyRole:
			userCompanyRoleIDs.append(usr.user.id)
		
		getFreeUsers = Users.objects.all().exclude(id__in=userCompanyRoleIDs)
		for user in getFreeUsers:
			freeUsers.append({
					"id": user.id,
					"name": user.name,
					"email": user.email,
					"status": user.active,
					"created_on": user.created_at
				})


		# Get UserCompanyRole
		getUserCompanyRole = UserCompanyRole.objects.filter(user=curr_user, 
															user__active=True,
															# company__id=request_data["company_id"],
															company__active=True, 
															role__active=True, 
															isActive=True)

		# Get all roles
		isAuthorized = False
		displayData = None
		allRoles = []
		for user in getUserCompanyRole:
			if user.role.role_name.upper() not in allRoles:
				allRoles.append(user.role.role_name.upper())

			if "SUPER-USER".upper() in allRoles:
				isAuthorized = True
				displayData = 'ALL'
			elif "COMPANY-ADMIN".upper() in allRoles:
				isAuthorized = True
				displayData = 'COMPANY-LEVEL'
			elif "PROJECT-ADMIN".upper() in allRoles:
				isAuthorized = True
				displayData = 'PROJECT-LEVEL'
		
		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company_id"]:
				apiParamsInfo[key] = value

		if isAuthorized:
			data = []
			companyData = []
			if displayData == "ALL":
				getUsersData = Users.objects.all()
				for user in getUsersData:
					getUserCompanyRole = UserCompanyRole.objects.filter(user=user, role__role_name="SUPER-USER")

					if len(getUserCompanyRole) == 0:
						data.append({
							"id": user.id,
							"name": user.name,
							"email": user.email,
							"status": user.active,
							"created_on": user.created_at
						})
			elif displayData in ["COMPANY-LEVEL"]:
				getUserCompanyRole = UserCompanyRole.objects.filter(company__id=request_data["company_id"])
				for usr in getUserCompanyRole:
					getUserCompanyRole = UserCompanyRole.objects.filter(user=usr.user, role__role_name="SUPER-USER")

					if len(getUserCompanyRole) == 0:
						data.append({
							"id": usr.user.id,
							"name": usr.user.name,
							"email": usr.user.email,
							"status": usr.user.active,
							"created_on": usr.user.created_at
						})

				data = data + freeUsers
			elif displayData in ["PROJECT-LEVEL"]:
				getUserCompanyRole = ProjectUsers.objects.filter(user__user=curr_user, user__company__id=request_data["company_id"])

				if len(getUserCompanyRole) > 0:
					getUserCompanyRole = getUserCompanyRole[0]
					getUserCompanyRole = ProjectUsers.objects.filter(project=getUserCompanyRole.project)
					for usr in getUserCompanyRole:
						getUserCompanyRole = UserCompanyRole.objects.filter(user=usr.user.user, role__role_name="SUPER-USER")

						if len(getUserCompanyRole) == 0:
							data.append({
								"id": usr.user.user.id,
								"name": usr.user.user.name,
								"email": usr.user.user.email,
								"status": usr.user.user.active,
								"created_on": usr.user.user.created_at
							})

					data = data + freeUsers
				else:
					data = freeUsers

			logs["data"]["status_message"] = "Users listed successfully."

			response["data"] = data
			response['message'] = "Users listed successfully."
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