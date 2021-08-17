from usermanagement.models import Users, AccessManagement, Roles
from usermanagement.utils.hash import encryption,decryption
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
import datetime

from organization.models import Company, CompanyInfo, UserCompanyRole

actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_get_company_info(request_data, token):
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

			response["message"] = "Invalid Token."
			response["statuscode"] = 500

			actvity_logs.insert_one(logs)
			return response
		else:
			curr_user = curr_user[0]
			logs["User"] = curr_user.id

			# Get UserCompanyRole
			getUserCompanyRole = UserCompanyRole.objects.filter(user=curr_user,
																user__active=True,
																#company__id=request_data["company_id"]
																company__active=True,
																role__active=True,
																isActive=True)

		# Get all roles
		isAuthorized = False
		allRoles = []
		for user in getUserCompanyRole:
			if user.role.role_name.upper() not in allRoles:
				allRoles.append(user.role.role_name.upper())

		if "SUPER-USER".upper() in allRoles:
			isAuthorized = True
		elif "COMPANY-ADMIN".upper() in allRoles:
			isAuthorized = True
		
		comapnyInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company_id"]:
				comapnyInfo[key] = value

		if isAuthorized:
			getCompany = Company.objects.filter(id=comapnyInfo["client_id"])
			getCompanyInfo=CompanyInfo.objects.filter(company=getCompany[0],active=True)
			# getCompanyUsers=UserCompanyRole.objects.filter(company=getCompany[0]
            #                                       ,role__role_name="COMPANY-ADMIN"
            #                                       , isActive=True)

			if len(getCompany) > 0 and len(getCompanyInfo):
				getCompanyData = getCompanyInfo.values()[0]
				getCompanyInfo=getCompanyInfo[0]
				getCompanyData["created_at"] = getCompanyInfo.created_at.strftime("%d-%m-%Y")
				getCompanyData["updated_at"] = getCompanyInfo.updated_at.strftime("%d-%m-%Y")
				getCompanyData["company_id"] = getCompanyInfo.company.id
				getCompanyData["name"] = getCompanyInfo.company.name
				response["data"] = getCompanyData
				logs["data"]["data_fields"] = [comapnyInfo["client_id"]]
				logs["data"]["status_message"] = "Company fetched successfully."
				response['message'] = 'Company fetched successfully.'
				response["statuscode"] = 200
			elif len(getCompany) > 0:
				getCompanyData = getCompany.values()[0]
				getCompanyData["created_at"] = getCompany[0].created_at.strftime("%d-%m-%Y")
				getCompanyData["updated_at"] = getCompany[0].updated_at.strftime("%d-%m-%Y")
				getCompanyData.pop('address2')
				response["data"] = getCompanyData
				logs["data"]["data_fields"] = [comapnyInfo["client_id"]]
				logs["data"]["status_message"] = "Company Information fetched successfully."

				response['message'] = 'Company Information fetched successfully.'
				response["statuscode"] = 200

			else:
				logs["data"]["data_fields"] = [comapnyInfo["client_id"]]
				logs["data"]["status_message"] = 'No Company Information found in database.'
				response['message'] = 'No Company Information found in database.'
				response["statuscode"] = 400
		else:
			logs["data"]["data_fields"] = [comapnyInfo["client_id"]]
			logs["data"]["status_message"] = 'Only SuperUser can fetch the Company Information.'
			response['message'] = 'Only SuperUser can fetch the Company Information.'
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

