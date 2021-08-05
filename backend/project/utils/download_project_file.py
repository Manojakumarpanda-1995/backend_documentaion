# from usermanagement.models import Users, AccessManagement, Roles
# from usermanagement.utils.hash import encryption, decryption, removeSpecialCharacters
# from django.conf import settings
# from django.db import IntegrityError
# import re
# import os
# import sys
# import logging
# import uuid
# import hashlib
# import datetime

# from organization.models import UserCompanyRole
# from project.models import BotFileUpload, GetProgress, ProjectUsers
# from project.tasks import trainingFileDownload, modelChainFileDownload

# secret = getattr(settings, "SECRET_KEY", None)
# actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
# error_logs = getattr(settings, "ERROR_LOGS_DB", None)


# def func_download_project_file(request_data, token):
# 	try:
# 		response={}

# 		# request_data["project_id"] = request_data["project_id"][0]
# 		# request_data["flag"] = request_data["flag"][0]
		
# 		logs = {
# 			"Client_IP_Address": request_data["Client_IP_Address"],
# 			"Remote_ADDR": request_data["Remote_ADDR"],
# 			"data": {
# 				"Requested_URL": request_data["Requested_URL"]
# 			},
# 			"BotID": request_data["project_id"]
# 		}

# 		curr_user = Users.objects.filter(token=token)
# 		if len(curr_user) == 0:
# 			logs["data"]["status_message"] = "Invalid Token."
# 			response['message'] = "Invalid Token."
# 			response["statuscode"] = 400

# 			actvity_logs.insert_one(logs)
# 			return response
# 		else:
# 			curr_user = curr_user[0]
# 			logs["User"] = curr_user.id

# 		flagValue = int(request_data["flag"])
		
# 		# Get BotUser
# 		getProjectUser = ProjectUsers.objects.filter(user__user=curr_user, project__project_id=request_data["project_id"])

# 		isAuthorized = False
# 		if len(getProjectUser) > 0:
# 			getProjectUser = getProjectUser[0]
# 			if flagValue == 2:
# 				if getProjectUser.user.role.role_name in ["SUPER-USER", "COMPANY-ADMIN", "PROJECT-ADMIN"]:
# 					isAuthorized = True
# 			elif flagValue == 999:
# 				if getProjectUser.user.role.role_name in ["SUPER-USER", "COMPANY-ADMIN", "PROJECT-ADMIN"]:
# 					isAuthorized = True
# 		else:
# 			getProjectUser = UserCompanyRole.objects.filter(user=curr_user, role__role_name="SUPER-USER")
# 			if len(getProjectUser) > 0:
# 				isAuthorized = True
# 			else:
# 				getProjectUser = ProjectUsers.objects.filter(project__project_id=request_data["project_id"])
# 				if len(getProjectUser) > 0:
# 					getProjectUser = UserCompanyRole.objects.filter(user=curr_user, company=getProjectUser.user.company, role__role_name="COMPANY-ADMIN")
# 					if len(getProjectUser) > 0:
# 						isAuthorized = True
		
# 		getGraph = GetProgress.objects.filter(user=curr_user)
# 		if len(getGraph) == 0:
# 			getGraph = GetProgress.objects.create(user=curr_user)
# 		else:
# 			getGraph = getGraph[0]


# 		apiParamsInfo = {}
# 		for key, value in request_data.items():
# 			if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company_id", "client_id"]:
# 				apiParamsInfo[key] = value

		
# 		if isAuthorized:
# 			if flagValue == 2:
# 				getGraph.download_training_file = {"message": "Downloading...", "isDownloading": True, "refreshedTime": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
# 				getGraph.save()

# 				# Celery Task
# 				trainingFileDownload.delay(str({"user_email": str(curr_user.email),
#                                                 "project_id": apiParamsInfo["project_id"]}))

# 			elif flagValue == 999:
# 				getGraph.download_model_chain = {"message": "Downloading...", "isDownloading": True, "refreshedTime": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
# 				getGraph.save()

# 				# Celery Task
# 				modelChainFileDownload.delay(str({"user_email": str(curr_user.email),
#                                                   "project_id": apiParamsInfo["project_id"]}))

# 			logs["data"]["data_fields"] = [apiParamsInfo["project_id"]]

# 			response["message"] = "File downloaded successfully."
# 			response["statuscode"] = 200
		
# 		else:
# 			logs["data"]["data_fields"] = [apiParamsInfo["project_id"]]

# 			response["message"] = "You are not authorized to perform the required action."
# 			response["statuscode"] = 400

# 		logs["added_at"] = datetime.datetime.utcnow()
# 		actvity_logs.insert_one(logs)
# 		return response

# 	except Exception as e:
# 		exc_type, exc_obj, exc_tb = sys.exc_info()
# 		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
# 		logging.info(str(exc_type) + " " + str(fname) + " " + str(exc_tb.tb_lineno) + " " + str(e))
# 		error_logs.insert_one({
# 			"error_type": str(exc_type),
# 			"file_name": str(fname),
# 			"line_no": str(exc_tb.tb_lineno),
# 			"error": str(e)
# 		})
# 		response["statuscode"] = 500
# 		return response