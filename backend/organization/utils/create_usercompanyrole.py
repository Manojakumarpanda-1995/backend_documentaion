from usermanagement.models import Users, AccessManagement, Roles
from usermanagement.utils.hash import encryption,decryption,generate_passwords,random_alphaNumeric_string
from django.conf import settings
from django.db import IntegrityError
import re
import os
import sys
import logging
import datetime

from project.models import ProjectUsers
from organization.models import Company, UserCompanyRole
from usermanagement.tasks import send_email

actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def func_create_usercompanyrole(request_data, token):
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
																# company__id=request_data["company_id"],
																company__active=True,
																role__active=True,
																isActive=True)

		# Get all roles
		# Superuser will only be superuser.
		isAuthorized = False
		roleIn = []
		allRoles = []
		for user in getUserCompanyRole:
			if user.role.role_name.upper() not in allRoles:
				allRoles.append(user.role.role_name.upper())

		if "SUPER-USER".upper() in allRoles:
			isAuthorized = True
			roleIn = ["COMPANY-ADMIN", "PROJECT-ADMIN", "USER"]
		elif "COMPANY-ADMIN".upper() in allRoles:
			roleIn = ["PROJECT-ADMIN", "USER"]
			isAuthorized = True
		elif "PROJECT-ADMIN".upper() in allRoles:
			roleIn = ["USER"]
			isAuthorized = True

		flag = request_data["flag"]
		
		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company_id", "flag"]:
				apiParamsInfo[key] = value

		if isAuthorized:
			isUser = False
			getUser = Users.objects.filter(id=apiParamsInfo["user"])
			if len(getUser) > 0:
				isUser = True
				getUser = getUser[0]
				#To check that the user is new or already exist with password not None
				if getUser.password is None:
					password=random_alphaNumeric_string(5,4)
					getUser.password=generate_passwords(password)
					getUser.save()
			else:
				logs["data"]["data_fields"] = [apiParamsInfo["user"]]
				logs["data"]["status_message"] = "User with the provided ID is not found in the database."
				response['message'] = "User with the provided ID is not found in the database."
				response["statuscode"] = 400
				return response

			isCompany = False
			getCompany = Company.objects.filter(id=apiParamsInfo["company"])
			if len(getCompany) > 0:
				isCompany = True
				getCompany = getCompany[0]
			else:
				logs["data"]["data_fields"] = [apiParamsInfo["company"]]
				logs["data"]["status_message"] = "Company with the provided ID is not found in the database."
				response['message'] = "Company with the provided ID is not found in the database."
				response["statuscode"] = 400
				return response
			

			isRole = False
			getRole = Roles.objects.filter(id=apiParamsInfo["role"])
			if len(getRole) > 0:
				getRole = getRole[0]
				if getRole.role_name in roleIn:
					isRole = True
			else:
				logs["data"]["data_fields"] = [apiParamsInfo["role"]]
				logs["data"]["status_message"] = "Role with the provided ID is not found in the database."
				response['message'] = "Role with the provided ID is not found in the database."
				response["statuscode"] = 400
				return response

			if isUser and isCompany and isRole:
				getUserCompanyRole = UserCompanyRole.objects.filter(user=getUser, company=getCompany, role=getRole, isActive=True)

				shouldCreated = False
				if flag == "COMPANY-MANAGEMENT":
					if len(getUserCompanyRole) == 0:
						getSuperUser = UserCompanyRole.objects.filter(user=getUser, isActive=True)
						allRoles = []
						for user in getSuperUser:
							if user.role.role_name.upper() not in allRoles:
								allRoles.append(user.role.role_name.upper())

						if "SUPER-USER" not in allRoles:
							getUserCompany = UserCompanyRole.objects.filter(user=getUser, company=getCompany)
							if len(getUserCompany) == 0:
								shouldCreated = True
							else:
								getUserCompanyUserRole = UserCompanyRole.objects.filter(user=getUser, company=getCompany, role__role_name="USER")

								if len(getUserCompanyUserRole) == 0:
									getUserCompanyUserRole = UserCompanyRole.objects.filter(user=getUser, company=getCompany, role__role_name="PROJECT-ADMIN", isActive=True)

									if len(getUserCompanyUserRole) == 0:
										shouldCreated = True
									else:
										logs["data"]["data_fields"] = [getUser.name, getCompany.name, getRole.role_name]
										logs["data"]["status_message"] = "User role cannot be upgraded from PROJECT-ADMIN to COMPANY-ADMIN in the present company."

										response['message'] = "User role cannot be upgraded from PROJECT-ADMIN to COMPANY-ADMIN in the present company."
										response["statuscode"] = 400
										logs["added_at"] = datetime.datetime.utcnow()
										actvity_logs.insert_one(logs)
										return response
								else:
									# Check whether COMPANY-ADMIN is in USERCOMPANYROLE
									getUserCompanyRoleUser =  UserCompanyRole.objects.filter(user=getUser, company=getCompany, role__role_name="COMPANY-ADMIN")
									if len(getUserCompanyRoleUser) > 0:
										getUserCompanyRoleUser = getUserCompanyRoleUser[0]
										getUserCompanyRoleUser.isActive = True
										getUserCompanyRoleUser.save()

										# Delete this user role
										getUserCompanyUserRole = getUserCompanyUserRole[0]
										getUserCompanyUserRole.isActive = False
										getUserCompanyUserRole.save()

										# Get All ProjectUsers Corresponding to this UserCompanyRole and delete them
										getProjectUsers = ProjectUsers.objects.filter(user=getUserCompanyUserRole)
										getProjectUsers.delete()
										# for projectUser in getProjectUsers:
										# 	projectUser.isActive = False
										# 	projectUser.save()

										# getUserCompanyUserRole.delete()
										getUserCompanyUserRole = getUserCompanyRoleUser
									else:
										getUserCompanyUserRole = getUserCompanyUserRole[0]
										getUserRole = Roles.objects.get(role_name="COMPANY-ADMIN")

										getUserCompanyUserRole.role = getUserRole
										getUserCompanyUserRole.save()

									logs["data"]["data_fields"] = [getUser.name, getCompany.name, getRole.role_name]
									logs["data"]["status_message"] = "User role has been upgraded from USER to COMPANY-ADMIN in the present company."

									response["data"] = getUserCompanyUserRole.id
									response["isNew"] = False
									response["isReplaced"] = True
									response['message'] = "User role has been upgraded from USER to COMPANY-ADMIN in the present company."
									response["statuscode"] = 200
									logs["added_at"] = datetime.datetime.utcnow()
									actvity_logs.insert_one(logs)
									return response
						else:
							logs["data"]["data_fields"] = [getUser.name, getCompany.name, getRole.role_name]
							logs["data"]["status_message"] = "SUPER-USER cannot be made COMPANY-ADMIN."

							response['message'] = "SUPER-USER cannot be made COMPANY-ADMIN."
							response["statuscode"] = 400
							logs["added_at"] = datetime.datetime.utcnow()
							actvity_logs.insert_one(logs)
							return response
					else:
						shouldCreated = True

				elif flag == "PROJECT-MANAGEMENT":
					if len(getUserCompanyRole) == 0:
						getSuperUser = UserCompanyRole.objects.filter(user=getUser, isActive=True)
						allRoles = []
						for user in getSuperUser:
							if user.role.role_name.upper() not in allRoles:
								allRoles.append(user.role.role_name.upper())

						if "SUPER-USER" not in allRoles:
							getUserCompany = UserCompanyRole.objects.filter(user=getUser, company=getCompany, isActive=True)
							if len(getUserCompany) == 0:
								shouldCreated = True
							else:
								getUserCompanyUserRole = UserCompanyRole.objects.filter(user=getUser, company=getCompany, role__role_name="USER", isActive=True)
								if len(getUserCompanyUserRole) == 0:
									getUserCompanyUserRole = UserCompanyRole.objects.filter(user=getUser, company=getCompany, role__role_name="COMPANY-ADMIN", isActive=True)

									if len(getUserCompanyUserRole) == 0:
										shouldCreated = True
									else:
										logs["data"]["data_fields"] = [getUser.name, getCompany.name, getRole.role_name]
										logs["data"]["status_message"] = "COMPANY-ADMIN cannot be made PROJECT-ADMIN."

										response['message'] = "COMPANY-ADMIN cannot be made PROJECT-ADMIN."
										response["statuscode"] = 400
										logs["added_at"] = datetime.datetime.utcnow()
										actvity_logs.insert_one(logs)
										return response
								else:
									shouldCreated = True
						else:
							logs["data"]["data_fields"] = [getUser.name, getCompany.name, getRole.role_name]
							logs["data"]["status_message"] = "SUPER-USER cannot be made COMPANY-ADMIN."

							response['message'] = "SUPER-USER cannot be made COMPANY-ADMIN."
							response["statuscode"] = 400
							logs["added_at"] = datetime.datetime.utcnow()
							actvity_logs.insert_one(logs)
							return response
					else:
						shouldCreated = True
				
				else:
					shouldCreated = True


				if shouldCreated:
					getUserCompanyRole = UserCompanyRole.objects.filter(user=getUser, company=getCompany, role=getRole)
					getUserRoles = UserCompanyRole.objects.filter(user=getUser)
					isNew=True if len(getUserRoles) else False
					if len(getUserCompanyRole) == 0:
						apiParamsInfo["created_by"] = curr_user
						apiParamsInfo["updated_by"] = apiParamsInfo["created_by"]

						apiParamsInfo["user"] = getUser
						apiParamsInfo["company"] = getCompany
						apiParamsInfo["role"] = getRole

						getUserCompanyRole = UserCompanyRole.objects.create(**apiParamsInfo)

						logs["data"]["data_fields"] = [getUser.name, getCompany.name, getRole.role_name]
						logs["data"]["status_message"] = "UserCompanyRole created successfully."

						response["data"] = getUserCompanyRole.id
						response["isNew"] = True
						response["isReplaced"] = False
						response['message'] = 'UserCompanyRole created successfully.'
						response["statuscode"] = 200

						# Send Email to new User
						getAccess = AccessManagement.objects.get(name=getUser)
						# if getAccess.last_login_attempt is None:
						# 	if getRole.role_name != "USER" and isNew==False:
						# 		send_email.delay(str({"email": getUser.email,
						# 							"subject": "New Registration",
						# 							"template_name": "generate_passwords", 
						# 							# "variables": [decryption(getUser.password)],
						# 							"variables": [password],
						# 							"email_type": "plain"
						# 							}))
						# 	elif getRole.role_name=='USER' and isNew==False:
						# 		send_email.delay(str({"email": getUser.email,
						# 							"subject": "New Registration",
						# 							# "template_name": "generate_passwords_user", 
						# 							"template_name": "generate_passwords", 
						# 							# "variables": [decryption(getUser.password)],
						# 							"variables": [password],
						# 							"email_type": "plain"
						# 							}))
						
						# else:
						# 	getUserCompany = getUserCompany[0]

						# 	logs["data"]["data_fields"] = [getUser.name, getCompany.name, getRole.role_name]
						# 	logs["data"]["status_message"] = "User in same company has already a role."

						# 	response["data"] = getUserCompany.id
						# 	response['message'] = "User in same company has already a role."
						# 	response["statuscode"] = 200
					else:
						getUserCompanyRole = getUserCompanyRole[0]
						getUserCompanyRole.isActive = True
						getUserCompanyRole.save()

						logs["data"]["data_fields"] = [getUser.name, getCompany.name, getRole.role_name]
						logs["data"]["status_message"] = "UserCompanyRole already existed."

						response["data"] = getUserCompanyRole.id
						response["isNew"] = False
						response["isReplaced"] = False
						response['message'] = 'UserCompanyRole already existed.'
						response["statuscode"] = 200
				else:
					logs["data"]["data_fields"] = [getUser.name, getCompany.name, getRole.role_name]
					logs["data"]["status_message"] = "The user cannot be given this role in the given company."

					response['message'] = "The user cannot be given this role in the given company."
					response["statuscode"] = 400
		else:
			logs["data"]["status_message"] = 'You cannot create the UserCompanyRole.'
			response['message'] = 'You cannot create the UserCompanyRole.'
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