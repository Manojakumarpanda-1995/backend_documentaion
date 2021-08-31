
import hashlib
import re
import faker
import pytest
from organization.models import *
from project.models import *
from usermanagement.models import *
from usermanagement.utils.hash import *
from project.models import ActivityLogs as ActivityLog


class Test_project_info():

	def test_all_project_info(self):
		assert ProjectInfo.objects.count()==Company.objects.count()
		getProject=ProjectInfo.objects.all()
		for x in range(len(getProject)):
			assert getProject[x].name=="{} project1".format(Company.objects.all()[x].name)
			assert getProject[x].project_id is not None
			assert getProject[x].description is not None
			assert getProject[x].catagory is not None
			assert getProject[x].salary_from is not None
			assert getProject[x].salary_to is not None
			assert getProject[x].start_date is not None
			assert getProject[x].start_time is not None
			assert getProject[x].end_time is not None
			assert getProject[x].created_by_id==1
			assert getProject[x].updated_by_id==1
   
	def test_project_info_models(self,setup_project_info):
     
		project=setup_project_info
		assert ProjectInfo.objects.count()==Company.objects.count()*2
		getProject=ProjectInfo.objects.all()
		for x in range(len(getProject)):
			assert getProject[x].project_id is not None
			assert getProject[x].description is not None
			assert getProject[x].catagory is not None
			assert getProject[x].salary_from is not None
			assert getProject[x].salary_to is not None
			assert getProject[x].start_date is not None
			assert getProject[x].start_time is not None
			assert getProject[x].end_time is not None
			assert getProject[x].created_by_id==1
			assert getProject[x].updated_by_id==1
   
	def test_project_users_models(self,setup_projectusers,setup_user_for_new_password):
		users=setup_user_for_new_password
		#one extra for projectadmin of microsoft
		assert ProjectUsers.objects.count()==(Company.objects.count()*len(users))+1 
		for projectuser in ProjectUsers.objects.all():
			assert projectuser.created_by_id==1
			assert projectuser.updated_by_id==1
			assert projectuser.isActive==1
   
	def test_file_upload(self,setup_fileupload):
		file_upload=setup_fileupload
		assert FileUpload.objects.count()==len(file_upload)
		getFileUpload=FileUpload.objects.all()
		for x in range(len(getFileUpload)):
			assert getFileUpload[x].original_file_name==file_upload[x]["original_file_name"]
			assert getFileUpload[x].datafile==file_upload[x]["datafile"]
			assert getFileUpload[x].function_type==file_upload[x]["function_type"]
			assert getFileUpload[x].created_by_id==file_upload[x]["created_by_id"]
			assert ".xlsx" in getFileUpload[x].original_file_name
			regex='[A-Z0-9a-z/]+[.]+xlsx'
			assert re.match(regex,str(getFileUpload[x].datafile))
   
	def test_file_download(self,setup_filedownload):
		file_download=setup_filedownload
		assert DownloadFile.objects.count()==len(file_download)
		getFileDownload=DownloadFile.objects.all()
		for x in range(len(getFileDownload)):
			assert getFileDownload[x].unique_string==file_download[x]["unique_string"]
			assert getFileDownload[x].datafile==file_download[x]["datafile"]
			assert getFileDownload[x].function_type==file_download[x]["function_type"]
			regex='[A-Z0-9a-z/]+[.]+xlsx'
			assert re.match(regex,str(getFileDownload[x].datafile))
   
	def test_activity_logs(self,setup_project_activitylog):
		activity_log=setup_project_activitylog
		assert ActivityLog.objects.count()==ProjectUsers.objects.count()
		getActivityLogs=ActivityLog.objects.all()
		for x in range(len(getActivityLogs)):
			assert getActivityLogs[x].activity==activity_log[x]["activity"]
			assert getActivityLogs[x].ip_address==activity_log[x]["ip_address"]
			
	def test_getprogress(self,setup_getprogress,setup_saved_user):
		assert GetProgress.objects.count()==Users.objects.count()
		for progress in GetProgress.objects.all():
			assert progress.user is not None
			assert progress.bulk_user_upload == '{}'
			assert progress.bulk_user_download =='{}'
			assert progress.base_file_upload =='{}'
			assert progress.get_user_logs=='{}'
