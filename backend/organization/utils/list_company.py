from usermanagement.models import Users, AccessManagement, Roles
from usermanagement.utils.hash import encryption,decryption
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
import datetime

from organization.models import UserCompanyRole, Company

actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_list_company(request_data, token):
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
																#company__id=request_data["company_id"],
																company__active=True, 
																role__active=True, 
																isActive=True)

		# Get all roles
		isAuthorized = False
		displayData = None
		isEditable = False
		allRoles = []

		for user in getUserCompanyRole:
			if user.role.role_name.upper() not in allRoles:
				allRoles.append(user.role.role_name.upper())
		
		if "SUPER-USER".upper() in allRoles:
			isAuthorized = True
			displayData = 'ALL'
			isEditable = True
		elif "COMPANY-ADMIN".upper() in allRoles:
			isAuthorized = True
			displayData = "COMPANY-LEVEL"
		elif "PROJECT-ADMIN".upper() in allRoles:
			isAuthorized = True
			displayData = "COMPANY-LEVEL"
		
		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company_id"]:
				apiParamsInfo[key] = value

		if isAuthorized:
			data = []

			if displayData == "ALL":
				companyAdded = []
				getCompanyData = Company.objects.all().exclude(id=1, name="Administrator")
				for company in getCompanyData:
					getCompanyAdmin = UserCompanyRole.objects.filter(company=company, role__role_name="COMPANY-ADMIN", isActive=True, user__active=True)
					if len(getCompanyAdmin) > 0:
						getCompanyAdmin = getCompanyAdmin[0]
						company_admin = getCompanyAdmin.user.email
						company_admin_id = getCompanyAdmin.user.id
					else:
						company_admin = None
						company_admin_id = None
					
					if company.id not in companyAdded and company_admin is not None:
						companyAdded.append(company.id)
						data.append({
							"id": company.id,
							"name": company.name,
							"partner_name": company.partner_name,
							"status": company.active,
							"created_on": company.created_at,
							"company_admin": company_admin,
							"company_admin_id": company_admin_id,
							"isEditable": isEditable,
							"isShow": True
						})
			else:
				companyAdded = []
				getUserCompanyRole = UserCompanyRole.objects.filter(user=curr_user, 
																	user__active=True,
																	company__active=True,
																	role__active=True, 
																	isActive=True)
				for usr in getUserCompanyRole:
					getCompanyUserRole = UserCompanyRole.objects.filter(company=usr.company, user=curr_user, isActive=True)
					allRoles = []

					shouldAdd = False

					for user in getCompanyUserRole:
						if user.role.role_name.upper() not in allRoles:
							allRoles.append(user.role.role_name.upper())

					if "SUPER-USER".upper() in allRoles:
						shouldAdd = True
					elif "COMPANY-ADMIN".upper() in allRoles:
						shouldAdd = True
					elif "PROJECT-ADMIN".upper() in allRoles:
						shouldAdd = True

					if shouldAdd:
						isShow = False
						getCompanyAdmin = UserCompanyRole.objects.filter(company=usr.company, role__role_name="COMPANY-ADMIN", isActive=True, user__active=True)
						if len(getCompanyAdmin) > 0:
							getCompanyAdmin = getCompanyAdmin[0]
							company_admin = getCompanyAdmin.user.email
							company_admin_id = getCompanyAdmin.user.id
						else:
							company_admin = None
							company_admin_id = None

						if getCompanyAdmin.user.id == curr_user.id:
							isShow = True
						
						if usr.company.id not in companyAdded:
							companyAdded.append(usr.company.id)
							data.append({
								"id": usr.company.id,
								"name": usr.company.name,
								"partner_name": usr.company.partner_name,
								"status": usr.company.active,
								"created_on": usr.company.created_at,
								"company_admin": company_admin,
								"company_admin_id": company_admin_id,
								"isEditable": isEditable,
								"isShow": isShow
							})

			logs["data"]["status_message"] = "List companies successfully."

			response["data"] = data
			response['message'] = "List companies successfully."
			response["statuscode"] = 200
		else:
			logs["data"]["status_message"] = "You are not authorized to list companies."

			response['message'] = "You are not authorized to list companies."
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