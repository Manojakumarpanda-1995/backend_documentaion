from usermanagement.models import Users, AccessManagement, Roles
from usermanagement.utils.hash import encryption, decryption, random_alphaNumeric_string,generate_passwords
from django.conf import settings
from django.db import IntegrityError
from django.utils import timezone
import re
import os
import sys
import logging
import uuid
import hashlib
import datetime

from organization.models import UserCompanyRole, Company
# from microsoftteamsproject.models import ProjectMetaData
from project.models import ProjectInfo, ProjectUsers
from usermanagement.tasks import send_email

verify_link_exp = getattr(settings, "VERIFICATION_LINK_EXPIRY_DURATION", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


def checkIfUserRoleCanBeCreated(user_email, role, project_id):
	canCreate = False
	returnMessage = "You cannot create a user with this role."
	statuscode = 400

	# Check If role is USER
	if role == "PROJECT-ADMIN":
		# Get Company
		getCompany = ProjectUsers.objects.filter(project__project_id=project_id)[0].user.company
		getUserCompanyRole = UserCompanyRole.objects.filter(user__email=user_email, isActive=True)
		isPossible = False
		if len(getUserCompanyRole) > 0:
			allRoles = []
			for user in getUserCompanyRole:
				if user.role.role_name.upper() not in allRoles:
					allRoles.append(user.role.role_name.upper())
			
			if ("SUPER-USER" not in allRoles):
				getUserCompanyRole = UserCompanyRole.objects.filter(user__email=user_email, company=getCompany, isActive=True)
				allRoles = []
				for user in getUserCompanyRole:
					if user.role.role_name.upper() not in allRoles:
						allRoles.append(user.role.role_name.upper())
				
				if ("COMPANY-ADMIN" not in allRoles):
					isPossible = True
				else:
					returnMessage = "Company-Admin cannot be made Project-Admin."
			else:
				returnMessage = "SUPER-USER cannot be made PROJECT-ADMIN."
		else:
			isPossible = True
		
		if isPossible:
			getProjectUsers = ProjectUsers.objects.filter(user__user__email=user_email, project__project_id=project_id, user__isActive=True, isActive=True)

			if len(getProjectUsers) > 0:
				allRoles = []
				for projectUser in getProjectUsers:
					if projectUser.user.role.role_name not in allRoles:
						allRoles.append(projectUser.user.role.role_name)
				
				if "USER" in allRoles:
					if "PROJECT-ADMIN" in allRoles:
						returnMessage = "User has projecth the role for the same project i.e. PROJECT-ADMIN and USER."
					else:
						# # Replace USER with PROJECT-ADMIN
						# getUserCompanyRoletoReplace = UserCompanyRole.objects.filter(user__email=user_email, company=getCompany, role__role_name="PROJECT-ADMIN")
						# if len(getUserCompanyRoletoReplace) > 0:
						# 	getUserCompanyRoletoReplace = getUserCompanyRoletoReplace[0]
							
						# 	# Check is it is Inactive
						# 	if not getUserCompanyRoletoReplace.isActive:
						# 		getUserCompanyRoletoReplace.isActive = True
						# 		getUserCompanyRoletoReplace.save()
						# else:
						# 	# Create User Company Role
						# 	getRole = Roles.objects.get(role_name="PROJECT-ADMIN")
						# 	getUserCompanyRoletoReplace = UserCompanyRole.objects.filter(user__email=user_email, company=getCompany, role__role_name="PROJECT-ADMIN")


						# getProjectUser = ProjectUsers.objects.get(user__user__email=user_email, 
						# 									 user__role__role_name="USER", 
						# 									 project__project_id=project_id, 
						# 									 user__isActive=True, 
						# 									 isActive=True)
						
						# getProjectUser.user = getUserCompanyRoletoReplace
						# getProjectUser.save()
						getRole = Roles.objects.get(role_name="PROJECT-ADMIN")
						getProjectUsers = ProjectUsers.objects.get(user__user__email=user_email, user__role__role_name="USER", project__project_id=project_id, user__isActive=True, isActive=True)

						getProjectUsers.user.role = getRole
						getProjectUsers.user.save()

						# Now delete role USER for same user
						getProjectUsersDelete = ProjectUsers.objects.filter(user__user__email=user_email, user__role__role_name="USER", project__project_id=project_id)
						getProjectUsersDelete.delete()

						returnMessage = "User role has been promoted from USER to PROJECT-ADMIN."
						statuscode = 200
				else:
					canCreate = True
			else:
				canCreate = True

	elif role == "USER":
		# Get Company
		getCompany = ProjectUsers.objects.filter(project__project_id=project_id)[0].user.company
		getUserCompanyRole = UserCompanyRole.objects.filter(user__email=user_email, isActive=True)
		
		isPossible = False
		if len(getUserCompanyRole) > 0:
			allRoles = []
			for user in getUserCompanyRole:
				if user.role.role_name.upper() not in allRoles:
					allRoles.append(user.role.role_name.upper())
			
			if ("SUPER-USER" not in allRoles):
				getUserCompanyRole = UserCompanyRole.objects.filter(user__email=user_email, company=getCompany, isActive=True)
				allRoles = []
				for user in getUserCompanyRole:
					if user.role.role_name.upper() not in allRoles:
						allRoles.append(user.role.role_name.upper())
				
				if ("COMPANY-ADMIN" not in allRoles):
					isPossible = True
				else:
					returnMessage = "COMPANY-ADMIN cannot be made USER."
			else:
				returnMessage = "SUPER-USER cannot be made USER."
		else:
			isPossible = True
		
		if isPossible:
			getProjectUsers = ProjectUsers.objects.filter(user__user__email=user_email, project__project_id=project_id, user__isActive=True, isActive=True)

			if len(getProjectUsers) > 0:
				allRoles = []
				for projectUser in getProjectUsers:
					if projectUser.user.role.role_name not in allRoles:
						allRoles.append(projectUser.user.role.role_name)
				
				if "PROJECT-ADMIN" in allRoles:
					returnMessage = "PROJECT-ADMIN cannot be made USER"
				else:
					canCreate = True
			else:
				canCreate = True
	return canCreate, returnMessage, statuscode


def func_create_project_user(request_data, token):
	try:
		response={}

		logs = {
			"Client_IP_Address": request_data["Client_IP_Address"],
			"Remote_ADDR": request_data["Remote_ADDR"],
			"data": {
				"Requested_URL": request_data["Requested_URL"]
			},
			"Project": request_data["project_id"]
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
			isAuthorized = True
			role = "SUPER-USER"
		elif "COMPANY-ADMIN" in allRoles:
			isAuthorized = True
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
			isAuthorized = True
			role = "PROJECT-ADMIN"

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

		else:
			logs["data"]["status_message"] = 'You are not authorized to create project user.'
			response['message'] = 'You are not authorized to create project.'
			response["statuscode"] = 400


		apiParamsInfo = {}
		for key, value in request_data.items():
			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company_id", "client_id"]:
				apiParamsInfo[key] = value

		if isAuthorized:
			# apiParamsInfo['password'] = encryption(random_alphaNumeric_string(5, 4))
			password =random_alphaNumeric_string(5, 4)
			apiParamsInfo['password'] = generate_passwords(password)
			apiParamsInfo['token'] = uuid.uuid4().hex
			apiParamsInfo['hashkey'] = uuid.uuid4().hex[:10]

			# Get Role
			getRole = Roles.objects.get(id=apiParamsInfo["user_role"])

			canCreate = False
			returnMessage = "You cannot create a user with this role."
			statuscode = 400

			if getRole.role_name == "USER":
				canCreate = True
			elif (getRole.role_name == "PROJECT-ADMIN") and (role in ["SUPER-USER", "COMPANY-ADMIN"]):
				canCreate = True
			
			if canCreate:
				# Function to check if the given role is good to go
				if apiParamsInfo["isUser"]:
					canCreate, returnMessage, statuscode = checkIfUserRoleCanBeCreated(apiParamsInfo["user_email"], getRole.role_name, apiParamsInfo["project_id"])

			if canCreate:
				# Get User
				if apiParamsInfo["isUser"]:
					getUser = Users.objects.get(email=apiParamsInfo["user_email"])
				else:
					first_name = None
					last_name = None
					name_list = []
					if "first_name" in apiParamsInfo:
						first_name = str(apiParamsInfo["first_name"]).strip()
						name_list.append(first_name)
					if "last_name" in apiParamsInfo:
						last_name = str(apiParamsInfo["last_name"]).strip()
						name_list.append(last_name)

					getUser = Users.objects.create(first_name=first_name,
												last_name=last_name,
												name=" ".join(name_list),
												email=apiParamsInfo["user_email"],
												password=apiParamsInfo["password"],
												token=apiParamsInfo["token"],
												hashkey=apiParamsInfo["hashkey"])

					# Access Management
					verify_expiry = timezone.now() + datetime.timedelta(minutes=verify_link_exp)
					AccessManagement.objects.create(name=getUser, password_attempts=0, verification_link_expiry=verify_expiry)
					#To chcek if the user is new or already exist
					getUserRoles = UserCompanyRole.objects.filter(user=getUser)
					isNew=True if len(getUserRoles) else False
					# Celery
					if getRole.role_name != "USER" and isNew==False:
						send_email.delay(str({"email": getUser.email,
											"subject": "New Registration",
											"template_name": "generate_passwords", 
											# "variables": [decryption(apiParamsInfo['password'])],
											"variables": [password],
											"email_type": "plain"
											}))
					elif getRole.role_name=="USER" and isNew==False:
						# Get Project
						getProject = ProjectInfo.objects.get(project_id=apiParamsInfo["project_id"])

						# Check if microsoft teams info for the project is available or not
						# projectMetaData = ProjectMetaData.objects.filter(project=getProject, isActive=True)
						projectMetaData = []
						if len(projectMetaData) > 0:
							send_email.delay(str({"email": getUser.email,
												"subject": "New Registration",
												 
												"template_name": "generate_passwords", 
												# "variables": [decryption(apiParamsInfo['password']),getUser.first_name, getUser.last_name, getProject.name, projectMetaData[0].mt_client_id],
												"variables": [password,getUser.first_name, getUser.last_name, getProject.name, projectMetaData[0].mt_client_id],
												"email_type": "plain"
												}))
						else:
							send_email.delay(str({"email": getUser.email,
												"subject": "New Registration",
												
												"template_name": "generate_passwords", 
												# "variables": [decryption(apiParamsInfo['password']),getUser.first_name, getUser.last_name, getProject.name],
												"variables": [password,getUser.first_name, getUser.last_name, getProject.name],
												"email_type": "plain"
												}))

				# Get Company
				getCompany = ProjectUsers.objects.filter(project__project_id=apiParamsInfo["project_id"])[0].user.company

				# Check whether user is already in the company with the same role
				getUserCompanyRole = UserCompanyRole.objects.filter(user=getUser, company=getCompany, role=getRole, isActive=True)

				if len(getUserCompanyRole) == 0:
					getUserCompanyRole = UserCompanyRole.objects.filter(user=getUser, company=getCompany, role=getRole)

					if len(getUserCompanyRole) == 0:
						getUserCompanyRole = UserCompanyRole.objects.create(user=getUser, company=getCompany, role=getRole, created_by=curr_user, updated_by=curr_user)
					else:
						getUserCompanyRole = getUserCompanyRole[0]
						getUserCompanyRole.isActive = True
						getUserCompanyRole.save()
				else:
					getUserCompanyRole = getUserCompanyRole[0]

				getProject = ProjectInfo.objects.get(project_id=apiParamsInfo["project_id"])

				# Get Project User
				getProjectUser = ProjectUsers.objects.filter(user=getUserCompanyRole, project=getProject)

				if len(getProjectUser) == 0:
					getProjectUser = ProjectUsers.objects.create(user=getUserCompanyRole, project=getProject, created_by=curr_user, updated_by=curr_user)
					if "expiry_date" in apiParamsInfo:
						getProjectUser.expiry_date = datetime.datetime.strptime(apiParamsInfo["expiry_date"], "%Y-%m-%d %H:%M")
						getProjectUser.save()

					response["data"] = getProjectUser.id

					logs["data"]["data_fields"] = [apiParamsInfo["user_email"], apiParamsInfo["project_id"]]
					logs["data"]["status_message"] = "User is created successfully."

					response['message'] = "User is created successfully."
					response["statuscode"] = 200
				else:
					getProjectUser = getProjectUser[0]
					response["data"] = getProjectUser.id

					logs["data"]["data_fields"] = [apiParamsInfo["user_email"], apiParamsInfo["project_id"]]
					logs["data"]["status_message"] = "User already has same role in the given company."

					response['message'] = "User already has same role in the given company."
					response["statuscode"] = 200
				# else:
				# 	logs["data"]["data_fields"] = [apiParamsInfo["user_email"], apiParamsInfo["project_id"]]
				# 	logs["data"]["status_message"] = "User already has a role in the given company."

				# 	response['message'] = "User already has a role in the given company."
				# 	response["statuscode"] = 400
			else:
				logs["data"]["data_fields"] = [apiParamsInfo["user_email"], apiParamsInfo["project_id"]]
				logs["data"]["status_message"] = returnMessage

				response['message'] = returnMessage
				response["statuscode"] = statuscode
		else:
			logs["data"]["status_message"] = 'Only SuperUser, Company-Admin and Project-Admin can create the project users.'
			response['message'] = 'Only SuperUser, Company-Admin and Project-Admin can create the project users.'
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