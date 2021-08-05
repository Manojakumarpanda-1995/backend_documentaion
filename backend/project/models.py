import os
import hashlib
import datetime
from django.db import models
from usermanagement.models import Users
from organization.models import UserCompanyRole

def get_file_path(instance, filename):
	s = instance.created_by.hashkey
	return os.path.join(str(s), filename)


class ProjectInfo(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=1000, blank=False, null=False)
	project_name_hash = models.CharField(max_length=255, blank=False, null=False, unique=True)
	description = models.TextField(blank=True, null=True)
	project_id = models.CharField(max_length=255, blank=False, null=False, unique=True)
	isActive = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE, related_name="project_created_by")
	updated_at = models.DateTimeField(auto_now=True)
	updated_by = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE, related_name="project_updated_by")


class ProjectUsers(models.Model):
	user = models.ForeignKey(UserCompanyRole, blank=False, null=False, on_delete=models.CASCADE)
	project = models.ForeignKey(ProjectInfo, blank=False, null=False, on_delete=models.CASCADE)
	isActive = models.BooleanField(default=True)
	expiry_date = models.DateTimeField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE, related_name="project_user_created_by")
	updated_at = models.DateTimeField(auto_now=True)
	updated_by = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE, related_name="project_user_updated_by")


class FileUpload(models.Model):
	id = models.AutoField(primary_key=True)
	original_file_name = models.TextField(blank=False, null=False,verbose_name='originalFilename')
	datafile = models.FileField(blank=False,null=False,upload_to=get_file_path,verbose_name='Datafile')
	function_type = models.TextField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE)

	def __str__(self):
		return self.original_file_name


class ActivityLogs(models.Model):
	id = models.AutoField(primary_key=True)
	project_user = models.ForeignKey(ProjectUsers,blank=False, null=False,on_delete=models.CASCADE)
	timestamp = models.DateTimeField(blank=False,null=False) 
	activity = models.TextField(blank=False, null=False)
	ip_address = models.CharField(max_length=200, blank=True, null=True)


class DownloadFile(models.Model):
	id = models.AutoField(primary_key=True)
	function_type = models.TextField(blank=True, null=True)
	datafile = models.FileField(blank=False, null=False)
	unique_string = models.TextField(blank=False, null=False)

class GetProgress(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE)
	bulk_user_upload = models.TextField(default={})
	bulk_user_download = models.TextField(default={})
	base_file_upload = models.TextField(default={})
	get_user_logs = models.TextField(default={})	
