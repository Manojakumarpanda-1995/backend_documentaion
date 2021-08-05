import string
import os
import ast
from django.conf import settings
from celery import shared_task
from celery.task import periodic_task
from django.db.models import Q
from django.core.files import File
import json
from django.utils import timezone
import uuid
import datetime
import re
import hashlib
import logging

import numpy as np
import pandas as pd
from bson import ObjectId
from xlrd import open_workbook
import time
# from pyfasttext import FastText
import shutil


from usermanagement.models import Users, Roles, AccessManagement
from organization.models import UserCompanyRole
from project.models import GetProgress, ProjectInfo, ProjectUsers, DownloadFile
from usermanagement.utils.send_email import SendEmail
from usermanagement.utils.hash import encryption, decryption, random_alphaNumeric_string,generate_passwords


base_dir = getattr(settings, "BASE_DIR", None)
verify_link_exp = getattr(settings, "VERIFICATION_LINK_EXPIRY_DURATION", None)
media_files = getattr(settings, "MEDIA_ROOT", None)
cron_job_time = getattr(settings, "CRON_JOB_TIME_LIST", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)

def getProjectUserbyProjectID(value):
	getProject = ProjectUsers.objects.filter(project__project_id=value)
	if len(getProject) > 0:
		return getProject[0]
	else:
		return None

#To validate email in the format of foo./_/+/123@some.com 
#0->invalid,1->valid
def validate_email(email):
	try:
		if (re.search("[!#$%^&*()?=,<>/]",email)):
			return 0
		else:
			regex='[A-Z0-9a-z._+-]+[@][a-z]+[.]+[a-z]{2,3}'
			match=re.match(regex,email)
			# match=re.findall(regex,email)
			return 1 if match else 0
	except Exception as e:
		pass

def checkForSuperUser(user_email):
	getUserCompanyRole = UserCompanyRole.objects.filter(user__email=user_email, isActive=True)
	allRoles = []

	for user in getUserCompanyRole:
		if user.role.role_name not in allRoles:
			allRoles.append(user.role.role_name)
	
	if "SUPER-USER" in allRoles:
		return True
	else:
		return False


def checkForCompanyProjectAdmin(user_email, project_id):
	# Check if project exits
	getProject = ProjectInfo.objects.filter(project_id=project_id)
	print("getproject",getProject)
	if len(getProject) > 0:
		getCompany = ProjectUsers.objects.filter(user__user__email=user_email, project__project_id=project_id, isActive=True, user__isActive=True)
		print("getcompany",getCompany)
		if len(getCompany) > 0:
			getCompany = getCompany[0].user.company
			print("getcompany2",getCompany)

			getUserCompanyRole = UserCompanyRole.objects.filter(user__email=user_email, company=getCompany, isActive=True)
			allRoles = []

			for user in getUserCompanyRole:
				if user.role.role_name not in allRoles:
					allRoles.append(user.role.role_name)
			
			print("allroles",allRoles)
			if "SUPER-USER" in allRoles:
				return True
			elif "COMPANY-ADMIN" in allRoles:
				return True
			elif "PROJECT-ADMIN" in allRoles:
				return True
			else:
				return False
		else:
			return False
	else:
		return True


@shared_task
def send_email(data):
	data = ast.literal_eval(data)
	email = data["email"]
	subject = data["subject"]
	template_name = data["template_name"]
	variables = data["variables"]
	email_type = data["email_type"]
	SendEmail(email, subject, template_name, variables, email_type)


@shared_task
def bulkUploadUsers(data):
	data = ast.literal_eval(data)
	columnsMap = {
		"User Email": "user_email",
		"First Name": "first_name",
		"Last Name": "last_name",
		"Expiry Date (DD-MM-YYYY)": "expiry_date",
		"Expiry Time (HH:MM)": "expiry_time",
		# "User Role": "role"
	}

	curr_user = Users.objects.get(email=data["user_email"])

	getGraph = GetProgress.objects.filter(user=curr_user)
	if len(getGraph) == 0:
		getGraph = GetProgress.objects.create(user=curr_user)
	else:
		getGraph = getGraph[0]

	df = pd.read_excel(io=os.path.join(media_files, data["file"]), sheet_name=data["sheet_name"])
	df = df.applymap(lambda x: x.strip() if type(x) == str else x)
	df = df.rename(columns=columnsMap)
	df["role"] = "User"
	df = df.assign(project_id=data["project_id"])
	df = df.assign(projectinfo=df.project_id.apply(getProjectUserbyProjectID))
	df = df.replace({np.nan: None})
	df = df.assign(isSuperUser=df.user_email.apply(checkForSuperUser))
	df = df.assign(isCompanyProjectAdmin=df.apply(lambda x: checkForCompanyProjectAdmin(x.user_email, x.project_id), axis=1))
	isValid = (int(df.isSuperUser.sum()) == 0) and (int(df.isCompanyProjectAdmin.sum()) == 0)

	# print(df)
	print(df.isSuperUser.sum())
	print(df.isCompanyProjectAdmin.sum())
	nonAvailableProjects = []
	if isValid:
		for row in df.itertuples():        
			isAuthorized = False

			if row.projectinfo is not None:
				getUser = Users.objects.filter(email=row.user_email)

				if len(getUser) > 0:
					getUser = getUser[0]

					first_name = ""
					last_name = ""
					if row.first_name is not None:
						first_name = str(row.first_name).strip()
					
					if row.last_name is not None:
						last_name = str(row.last_name).strip()

					user_name = " ".join([first_name, last_name])

					getUser.first_name = first_name
					getUser.last_name = last_name
					getUser.name = user_name
					getUser.save()
				else:
					# password = encryption(random_alphaNumeric_string(5, 4))
					password = random_alphaNumeric_string(5, 4)
					token = uuid.uuid4().hex
					hashkey = str(uuid.uuid4().hex)[:10]

					first_name = ""
					last_name = ""
					if row.first_name is not None:
						first_name = str(row.first_name).strip()
					
					if row.last_name is not None:
						last_name = str(row.last_name).strip()

					user_name = " ".join([first_name, last_name])

					getUser = Users.objects.create(first_name=row.first_name,
													last_name=row.last_name,
													name=user_name, 
													email=row.user_email,
													# password=password,
													password=generate_passwords(password),
													token=token,
													hashkey=hashkey,
													designation=None)

					verify_expiry = timezone.now() + datetime.timedelta(minutes=verify_link_exp)
					curr_access = AccessManagement.objects.create(name=getUser, password_attempts=0, verification_link_expiry=verify_expiry)
					
					# Send Email to new user
					send_email(str({"email": getUser.email,
									"subject": "New Registration",
									"template_name": "generate_passwords", 
									# "variables": [decryption(password)],
									"variables": [password],
									"email_type": "plain"
									}))

				if row.expiry_date is not None:
					if type(row.expiry_date) == str:
						expiry_date = datetime.datetime.strptime(row.expiry_date, "%d-%m-%Y")
					else:
						expiry_date = row.expiry_date
					
					if row.expiry_time is not None:
						if type(row.expiry_time) == str:
							expiry_time = datetime.datetime.strptime(":".join(row.expiry_date.split(":")[:2]), "%I:%M")
						else:
							expiry_time = row.expiry_time
						expiry_date = datetime.datetime.combine(expiry_date, expiry_time)
				else:
					expiry_date = row.expiry_date


				# Check User Company
				getUserCompanyRole = UserCompanyRole.objects.filter(user=getUser, company=row.projectinfo.user.company, role__role_name=row.role.upper())

				if len(getUserCompanyRole) == 0:
					getRole = Roles.objects.get(role_name=row.role.upper())
					getUserCompanyRole = UserCompanyRole.objects.create(user=getUser, 
																		company=row.projectinfo.user.company, 
																		role=getRole,
																		created_by=curr_user,
																		updated_by=curr_user)
				else:
					getUserCompanyRole = getUserCompanyRole[0]
				
				# Get Project User
				getProjectUser = ProjectUsers.objects.filter(project=row.projectinfo.project, user=getUserCompanyRole)

				if len(getProjectUser) == 0:
					getProjectUser = ProjectUsers.objects.create(project=row.projectinfo.project, 
														user=getUserCompanyRole, 
														created_by=curr_user,
														updated_by=curr_user,
														expiry_date=expiry_date)
				else:
					getProjectUser = getProjectUser[0]
					getProjectUser.updated_by = curr_user
					getProjectUser.expiry_date = expiry_date
					getProjectUser.save()

			else:
				if row.project_id not in nonAvailableProjects:
					nonAvailableProjects.append(row.project_id)

		getGraph.bulk_user_upload = json.dumps({
			"message": "Done...", 
			"isUploading": False,
			"isError": False,
			"Non-AvailableProjects": nonAvailableProjects, 
			"refreshedTime": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")})
	else:
		getGraph.bulk_user_upload = json.dumps({
			"message": "Done...", 
			"isUploading": False,
			"isError": True,
			"errorMessage": "SUPER-USER, COMPANY-ADMIN and PROJECT-ADMIN of the same project cannot be made USER.",
			"Non-AvailableProjects": nonAvailableProjects, 
			"refreshedTime": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")})

	getGraph.save()

	# Add Logs
	logs = {
		"User": curr_user.id,
		"data": {
			"Requested_URL": "Bulk Upload Users",
			"data_fields": [data["file"]],
			"status_message": "Bulk upload users successfully."
		},
		"isCeleryTask": True,
		"added_at": datetime.datetime.utcnow()
	}

	actvity_logs.insert_one(logs)

@shared_task
def bulkDownloadUsers(data):
	data = ast.literal_eval(data)
	curr_user = Users.objects.get(email=data["user_email"])

	getGraph = GetProgress.objects.filter(user=curr_user)
	if len(getGraph) == 0:
		getGraph = GetProgress.objects.create(user=curr_user)
	else:
		getGraph = getGraph[0]

	
	columnsMap = {
		"user__user__first_name": "First_Name",
		"user__user__last_name": "Last_Name",
		"user__user__designation": "Designation",
		"user__user__email": "User_Email",
		"expiry_date_c": "Expiry_Date",
		"user__company__name": "User_Company",
		"user__role__role_name": "User_Role",
		"project__name": "Project_Name",
		"expiry_time": "Expiry_Time",
		"isActive": "Status"
	}

	
	getProjectUsers = ProjectUsers.objects.filter(project__project_id=data["project_id"]).values("id",
																			 "user__user__first_name",
																			 "user__user__last_name",
																			 "user__user__designation",
																			 "user__user__email",
																			 "expiry_date",
																			 "user__role__role_name",
																			 "project__name",
																			 "isActive")

	getProjectUsers = pd.DataFrame(list(getProjectUsers))

	if not getProjectUsers.empty:
		# getProjectUsers.user__user__expiry_date = getProjectUsers.user__user__expiry_date.dt.tz_convert(None)
		getProjectUsers.expiry_date = getProjectUsers.expiry_date.apply(lambda x: x.tz_convert(None) if not pd.isnull(x) else x)
		getProjectUsers = getProjectUsers.assign(expiry_time=getProjectUsers.expiry_date.apply(lambda x: x.strftime("%H:%M") if not pd.isnull(x) else None))
		getProjectUsers = getProjectUsers.assign(expiry_date_c=getProjectUsers.expiry_date.apply(lambda x: x.strftime("%d-%m-%Y") if not pd.isnull(x) else None))

		if data["role"] == "PROJECT-ADMIN":
			getProjectUsers = getProjectUsers.assign(is_editable=getProjectUsers.user__role__role_name.apply(lambda x: True if x == "USER" else False))
		elif data["role"] != "USER":
			getProjectUsers = getProjectUsers.assign(is_editable=getProjectUsers.user__role__role_name.apply(lambda x: True if x in ["USER", "PROJECT-ADMIN"] else False))
		else:
			getProjectUsers = getProjectUsers.assign(is_editable=False)

		# Remove Super User from the list
		getProjectUsers = getProjectUsers[~getProjectUsers.user__role__role_name.isin(['SUPER-USER', 'COMPANY-ADMIN'])]

		getProjectUsers.rename(columns=columnsMap, inplace=True)
		getProjectUsers = getProjectUsers[["id", "First_Name", "Last_Name", "User_Email", "User_Role", "Expiry_Date", "Expiry_Time", "Status", "is_editable"]]

		# Create Download File Entry
		# getDownload = DownloadFile.objects.create(function_type="BULK-DOWNLOAD", 
		# 										  unique_string=hashlib.sha256(str(datetime.datetime.utcnow().isoformat()).encode()).hexdigest(), 
		# 										  datafile="bulk_download/bulk_download.xlsx",
		# 										  expiry_time=timezone.now() + datetime.timedelta(seconds=file_download_link_exp))
		# getDownload.datafile = os.path.join(os.path.dirname(str(getDownload.datafile)), getDownload.unique_string + ".xlsx")
		# getDownload.save()

		# if not os.path.isdir(os.path.join(media_files, os.path.dirname(str(getDownload.datafile)))):
		# 	os.makedirs(os.path.join(media_files, os.path.dirname(str(getDownload.datafile))))
		
		# getProjectUsers.to_excel(os.path.join(media_files, str(getDownload.datafile)), index=False)

		user_data = getProjectUsers.to_dict("index")

		getGraph.bulk_user_download = json.dumps({
			"message": "Data retrieved successfully.", 
			"isDownloading": False,
			"isData": True,
			"data": user_data,
			"refreshedTime": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
		})

	else:
		getGraph.bulk_user_download = json.dumps({
			"message": "No data found!", 
			"isDownloading": False,
			"isData": False,
			"data": None,
			"refreshedTime": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
		})
	getGraph.save()

	# Add Logs
	logs = {
		"User": curr_user.id,
		"data": {
			"Requested_URL": "Bulk Download Users",
			"data_fields": [data["project_id"]],
			"status_message": "Bulk download users successfully."
		},
		"isCeleryTask": True,
		"ProjectID": data["project_id"],
		"added_at": datetime.datetime.utcnow()
	}

	actvity_logs.insert_one(logs)

# @periodic_task(run_every=datetime.timedelta(days=cron_job_time[0], hours=cron_job_time[1], minutes=cron_job_time[2], seconds=cron_job_time[3]))
def deactivateProjectUsersExpired():
	# Deactivate Project Users who are expired
	getProjectUsers = ProjectUsers.objects.all()

	for projectUser in getProjectUsers:
		if projectUser.expiry_date is not None:
			if projectUser.expiry_date < timezone.now():
				projectUser.isActive = False
				projectUser.save()
				
				
URLMetaDict = {
	"/project/create-module": ["Create New Module", "Description to be added", 0],
	"/project/list-module": ["List Modules", "Description to be added", 0],
	"/project/edit-module": ["Edit a Module", "Description to be added", 0],
	"/project/deactivate-module": ["Deactivate Module", "Description to be added", 0],
	"/project/create-project": ["Create New Project", "Description to be added", 3],
	"/project/assign-project": ["Assign Project", "Description to be added", 1],
	"/project/list-project": ["List Projects", "Description to be added", 0],
	"/project/list-project-byemail": ["List Projects", "Description to be added", 0],
	"/project/edit-project": ["Edit a project", "Description to be added", 1],
	"/project/delete-project": ["Delete a project", "Description to be added", 0],
	"/project/bulk-user-upload": ["Bulk users upload file", "Description to be added", 0],
	"/project/upload-project-file": ["Uploaded a project file", "Description to be added", 2],
	"/project/download-project-file": ["Download project file", "Description to be added", 2],
	"/project/download-file": ["Download file", "Description to be added", 4],
	"/project/download-large-file": ["Download file", "Description to be added", 4],
	"/project/get-progress": ["Get Progress", "Description to be added", 0],
	"/project/get-project-doc-ids": ["Get project data Mongo IDs", "Description to be added", 2],
	"/project/get-project-doc-by-id": ["Get project data from Mongo IDs", "Description to be added", 2],
	"/project/save-project-answer": ["Save new answer in MongoDB", "Description to be added", 2],
	"/project/start-project-model-training": ["Start project training", "Description to be added", 2],
	"/project/stop-project-model-training": ["Stop project training", "Description to be added", 2],
	"/project/get-model-training-progress": ["Get model training progress", "Description to be added", 0],
	"/project/project-response": ["Get project response", "Description to be added", 2],
	"/project/project-response-feedback": ["Save project response feedback", "Description to be added", 2],
	"/project/project-chat-history": ["Get project chat history", "Description to be added", 2],
	"/project/generate-user-logs": ["Get user logs", "Description to be added", 2],
	"/project/generate-training-logs": ["Get project training logs", "Description to be added", 2]
}


getProjectIDfromURL = {
	"/project/create-project": ["Create New Project", "Description to be added", 3],
	"/project/assign-project": ["Assign Project", "Description to be added", 1],
	"/project/list-project": ["List Projects", "Description to be added", 0],
	"/project/list-project-byemail": ["List Projects", "Description to be added", 0],
	"/project/edit-project": ["Edit a project", "Description to be added", 1],
	"/project/delete-project": ["Delete a project", "Description to be added", 0],
	"/project/bulk-user-upload": ["Bulk users upload file", "Description to be added", 0],
	"/project/upload-project-file": ["Uploaded a project file", "Description to be added", 2],
	"/project/download-project-file": ["Download project file", "Description to be added", 2],
	"/project/download-file": ["Download file", "Description to be added", 4],
	"/project/download-large-file": ["Download file", "Description to be added", 4],
	"/project/get-progress": ["Get Progress", "Description to be added", 0],
	"/project/get-project-doc-ids": ["Get project data Mongo IDs", "Description to be added", 2],
	"/project/get-project-doc-by-id": ["Get project data from Mongo IDs", "Description to be added", 2],
	"/project/save-project-answer": ["Save new answer in MongoDB", "Description to be added", 2],
	"/project/start-project-model-training": ["Start project training", "Description to be added", 2],
	"/project/stop-project-model-training": ["Stop project training", "Description to be added", 2],
	"/project/get-model-training-progress": ["Get model training progress", "Description to be added", 0],
	"/project/project-response": ["Get project response", "Description to be added", 2],
	"/project/project-response-feedback": ["Save project response feedback", "Description to be added", 2],
	"/project/project-chat-history": ["Get project chat history", "Description to be added", 2],
	"/project/generate-user-logs": ["Get user logs", "Description to be added", 2],
	"/project/generate-training-logs": ["Get project training logs", "Description to be added", 2]
}


def getURLMetaData(value):
	if value["Requested_URL"] in URLMetaDict:
		return [value["Requested_URL"]] + URLMetaDict[value["Requested_URL"]]
	else:
		return [value["Requested_URL"], None, None, 0]


def getProject(value):
	pass


@shared_task
def userLogs(data):
	data = ast.literal_eval(data)

	curr_user = Users.objects.get(email=data["user_email"])

	getGraph = GetProgress.objects.filter(user=curr_user)
	if len(getGraph) == 0:
		getGraph = GetProgress.objects.create(user=curr_user)
	else:
		getGraph = getGraph[0]

	role = data["role"]
	start_date = datetime.datetime.strptime(data["start_date"], "%Y-%m-%d")
	end_date = datetime.datetime.strptime(data["end_date"] + " 23:59:59", "%Y-%m-%d %H:%M:%S")

	# Add date filter
	getData = actvity_logs.find({"added_at":{"$gte": start_date,"$lte": end_date}})
	
	if getData.count() > 0:
		getData = pd.DataFrame(list(getData))

		if role == "SUPER-USER":
			getData = getData.assign(urlMeta=getData.data.apply(getURLMetaData))
			getData = getData.assign(isLog=getData.urlMeta.apply(lambda x: x[3]))
			getData = getData[getData.isLog != 0]
			getData = getData[getData.ProjectID == data["project_id"]]
			getData = getData.assign(project=getData.ProjectID.apply(lambda x: ProjectInfo.objects.get(project_id=x) if not pd.isnull(x) else x))
			getData = getData.assign(project_name=getData.project.apply(lambda x: x.name))
			getData = getData.assign(api_name=getData.urlMeta.apply(lambda x: x[1]))
			getData = getData.assign(api_url=getData.urlMeta.apply(lambda x: x[0]))
			getData = getData.assign(remark=getData.data.apply(lambda x: x["status_message"] if "status_message" in x else None))
			getData = getData.assign(user=getData.User.apply(lambda x: Users.objects.get(id=x) if not pd.isnull(x) else None))
			getData = getData.assign(user_name=getData.user.apply(lambda x: x.name if not pd.isnull(x) else None))
			getData = getData.assign(date=getData.added_at.apply(lambda x: x.strftime("%d-%m-%Y %H:%M:%S")))

			getData = getData[["api_name", "user_name", "project_name", "date"]]
			
			getData.rename(columns={
				"api_name": "API Name",
				"user_name": "User Name",
				"project_name": "Project Name",
				"date": "Date"
			}, inplace=True)

			user_logs = getData.to_dict("list")

		elif role == "COMPANY-ADMIN":
			getData = getData.assign(urlMeta=getData.data.apply(getURLMetaData))
			getData = getData.assign(isLog=getData.urlMeta.apply(lambda x: x[3]))
			getData = getData[getData.isLog != 0]
			getData = getData[getData.ProjectID == data["project_id"]]
			getData = getData.assign(project=getData.ProjectID.apply(lambda x: ProjectInfo.objects.get(project_id=x) if not pd.isnull(x) else x))
			getData = getData.assign(project_name=getData.project.apply(lambda x: x.name))
			getData = getData.assign(api_name=getData.urlMeta.apply(lambda x: x[1]))
			getData = getData.assign(api_url=getData.urlMeta.apply(lambda x: x[0]))
			getData = getData.assign(remark=getData.data.apply(lambda x: x["status_message"] if "status_message" in x else None))
			getData = getData.assign(user=getData.User.apply(lambda x: Users.objects.get(id=x) if not pd.isnull(x) else None))
			getData = getData.assign(user_name=getData.user.apply(lambda x: x.name if not pd.isnull(x) else None))
			getData = getData.assign(date=getData.added_at.apply(lambda x: x.strftime("%d-%m-%Y %I:%M:%S")))

			getData = getData[["api_name", "user_name", "project_name", "date"]]
			
			getData.rename(columns={
				"api_name": "API Name",
				"user_name": "User Name",
				"project_name": "Project Name",
				"date": "Date"
			}, inplace=True)

			user_logs = getData.to_dict("list")

		elif role == "PROJECT-ADMIN":
			getData = getData.assign(urlMeta=getData.data.apply(getURLMetaData))
			getData = getData.assign(isLog=getData.urlMeta.apply(lambda x: x[3]))
			getData = getData[getData.isLog != 0]
			getData = getData[getData.ProjectID == data["project_id"]]
			getData = getData.assign(project=getData.ProjectID.apply(lambda x: ProjectInfo.objects.get(project_id=x) if not pd.isnull(x) else x))
			getData = getData.assign(project_name=getData.project.apply(lambda x: x.name))
			getData = getData.assign(api_name=getData.urlMeta.apply(lambda x: x[1]))
			getData = getData.assign(api_url=getData.urlMeta.apply(lambda x: x[0]))
			getData = getData.assign(remark=getData.data.apply(lambda x: x["status_message"] if "status_message" in x else None))
			getData = getData.assign(user=getData.User.apply(lambda x: Users.objects.get(id=x) if not pd.isnull(x) else None))
			getData = getData.assign(user_name=getData.user.apply(lambda x: x.name if not pd.isnull(x) else None))
			getData = getData.assign(date=getData.added_at.apply(lambda x: x.strftime("%d-%m-%Y %I:%M:%S")))

			getData = getData[["api_name", "user_name", "project_name", "date"]]
			
			getData.rename(columns={
				"api_name": "API Name",
				"user_name": "User Name",
				"project_name": "Project Name",
				"date": "Date"
			}, inplace=True)

			user_logs = getData.to_dict("list")

		elif role == "USER":
			getData = getData.assign(urlMeta=getData.data.apply(getURLMetaData))
			getData = getData.assign(isLog=getData.urlMeta.apply(lambda x: x[3]))
			getData = getData[getData.isLog != 0]
			getData = getData[getData.ProjectID == data["project_id"]]
			getData = getData.assign(project=getData.ProjectID.apply(lambda x: ProjectInfo.objects.get(project_id=x) if not pd.isnull(x) else x))
			getData = getData.assign(project_name=getData.project.apply(lambda x: x.name))
			getData = getData.assign(api_name=getData.urlMeta.apply(lambda x: x[1]))
			getData = getData.assign(api_url=getData.urlMeta.apply(lambda x: x[0]))
			getData = getData.assign(remark=getData.data.apply(lambda x: x["status_message"] if "status_message" in x else None))
			getData = getData.assign(user=getData.User.apply(lambda x: Users.objects.get(id=x) if not pd.isnull(x) else None))
			getData = getData.assign(user_name=getData.user.apply(lambda x: x.name if not pd.isnull(x) else None))
			getData = getData.assign(date=getData.added_at.apply(lambda x: x.strftime("%d-%m-%Y %I:%M:%S")))

			getData = getData[["api_name", "user_name", "project_name", "date"]]
			
			getData.rename(columns={
				"api_name": "API Name",
				"user_name": "User Name",
				"project_name": "Project Name",
				"date": "Date"
			}, inplace=True)

			user_logs = getData.to_dict("list")

		getGraph.get_user_logs = json.dumps({
			"message": "Data retrieved successfully.",
			"data": user_logs,
			"isData": True, 
			"isGenerating": False, 
			"refreshedTime": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
		})
	
	else:
		getGraph.get_user_logs = json.dumps({
			"message": "No Data.",
			"isData": False, 
			"isGenerating": False, 
			"refreshedTime": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
		})

	getGraph.save()

	# Add Logs
	logs = {
		"User": curr_user.id,
		"data": {
			"Requested_URL": "User Logs",
			"data_fields": [data["project_id"]],
			"status_message": "User logs retrieved successfully."
		},
		"isCeleryTask": True,
		"ProjectID": data["project_id"],
		"added_at": datetime.datetime.utcnow()
	}

	actvity_logs.insert_one(logs)				
