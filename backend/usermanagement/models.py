from django.db import models
from django.core.validators import validate_email
import os

# Create your models here.
class Users(models.Model):
	id = models.AutoField(primary_key=True,db_column='id')
	first_name = models.CharField(max_length=1000, blank=True, null=True)
	last_name = models.CharField(max_length=1000, blank=True, null=True)
	name = models.CharField(max_length=1000, blank=True, null=True)
	email = models.CharField(max_length=255, blank=True, null=True, unique=True, validators=[validate_email]) 
	password = models.TextField(blank=True,null=True)
	token = models.CharField(max_length=500, blank=True, null=True)
	# staff_id = models.IntegerField(blank=True, null=True, unique=True)
	designation = models.CharField(max_length=500, blank=True, null=True)
	active= models.NullBooleanField(default=True)
	user_verified = models.NullBooleanField(default=True) #email verification
	expiry_date = models.DateTimeField(blank=True,null=True)
	reporting_manager_id= models.IntegerField(blank=True, null=True)
	reporting_manager_name= models.CharField(max_length=500, blank=True, null=True)
	reporting_manager_email= models.CharField(max_length=500, blank=True, null=True, validators=[validate_email])
	hashkey = models.CharField(max_length=200, blank=True, null=True) 
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table="Users"
	
class AccessManagement(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.ForeignKey(Users,blank=True, null=True,on_delete=models.CASCADE)
	password_attempts =  models.IntegerField(blank=False, null=False, default=0)
	last_login_attempt=models.DateTimeField(blank=True,null=True)
	otp = models.CharField(max_length=2048, blank=True, null=True)
	otp_expiry_time = models.DateTimeField(blank=True,null=True)
	last_otp_attempt=models.DateTimeField(blank=True,null=True)
	otp_attempts =  models.IntegerField(blank=False, null=False, default=0)
	last_password_reset_request = models.DateTimeField(blank=True,null=True)
	password_reset_request_count = models.IntegerField(blank=False, null=False, default=0)
	verification_link_expiry=models.DateTimeField(blank=True,null=True)

	class Meta:
		db_table="AccessManagement"

class Roles(models.Model):
	id = models.AutoField(primary_key=True,db_column='id')
	role_name  = models.CharField(max_length=100, blank=False, null=False,unique=True)  
	role_description  = models.TextField(blank=True,null=True)
	active= models.BooleanField(default=1)
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE, related_name="role_created_by")
	updated_at = models.DateTimeField(auto_now=True)
	updated_by = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE, related_name="role_updated_by")

	class Meta:
		db_table="Roles"

class TemporaryURL(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(Users,blank=False, null=False,on_delete=models.CASCADE)
	expiry_time = models.DateTimeField(blank=False,null=False) 
	token=models.TextField(blank=False, null=False)
	filename=models.TextField(blank=False, null=False)
	filepath=models.TextField(blank=False, null=False)

	class Meta:
		db_table="TemporaryUrl"

class ActivityLogs(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(Users,blank=False, null=False,on_delete=models.CASCADE)
	timestamp = models.DateTimeField(blank=False,null=False) 
	activity = models.TextField(blank=False, null=False)
	ip_address = models.CharField(max_length=200, blank=True, null=True)

	class Meta:
		db_table="ActivityLogs"

class Workers(models.Model):
	id			=models.AutoField(primary_key=True,unique=True,db_column="id")
	name		=models.CharField(max_length=200,blank=False,null=False,db_column="Name of Worker")
	email		=models.CharField(max_length=250,blank=False,null=False,db_column="Email")
	phone_no	=models.CharField(max_length=13,blank=True,null=True,db_column="Ph.No")
	active		=models.BooleanField(default=True)
	created_at 	= models.DateTimeField(auto_now_add=True)
	updated_at 	= models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name
	
	class Meta:
		db_table="Workers"
		ordering=["-created_at"]

class AccessRequest(models.Model):
	id				=models.AutoField(primary_key=True,unique=True,db_column="id")
	name			=models.CharField(max_length=200,blank=False,null=False,db_column="Name of Worker")
	email			=models.CharField(max_length=250,blank=False,null=False,db_column="Email")
	company_name	=models.CharField(max_length=500,blank=True,null=False,db_column="Company Name")
	phone_number	=models.CharField(max_length=13,blank=True,null=True,db_column="Ph.No")
	skill_sets		=models.TextField(blank=True,null=True,db_column="Skill Sets")
	active			=models.BooleanField(default=True)
	pending_status 	=models.BooleanField(default=True)
	created_at 		= models.DateTimeField(auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name
	
	class Meta:
		db_table="AccessRequest"
		ordering=["-created_at"]



