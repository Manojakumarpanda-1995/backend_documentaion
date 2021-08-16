import os
import logging
from django.core.validators import validate_email
from django.db import models
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from usermanagement.models import Roles, Users


def get_file_path(instance, filename):
	s = instance.company.name
	return os.path.join(str(s), filename)

class Company(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=1000, blank=False, null=False)
	address1 = models.CharField(max_length=1000, blank=True, null=True)
	address2 = models.CharField(max_length=1000, blank=True, null=True)
	city = models.CharField(max_length=100, blank=True, null=True)
	state = models.CharField(max_length=100, blank=True, null=True)
	country = models.CharField(max_length=100, blank=True, null=True)
	# country_code = models.CharField(max_length=100, blank=True, null=True)
	partner_name = models.CharField(max_length=100, blank=True, null=True)
	state_pin_code = models.CharField(max_length=100, blank=True, null=True)
	active= models.BooleanField(default=1)
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE, related_name="company_created_by")
	updated_at = models.DateTimeField(auto_now=True)
	updated_by = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE, related_name="company_updated_by")

	class Meta:
		db_table="Company"

class CompanyInfo(models.Model):
	id = models.AutoField(primary_key=True)
	company = models.ForeignKey(Company,on_delete=models.CASCADE,blank=True,null=True)
	logo = models.ImageField(upload_to=get_file_path,blank=True, null=True)
	corporate_type = models.CharField(max_length=1000, blank=True, null=True)
	number_of_emploies= models.CharField(max_length=100, blank=True, null=True)
	type= models.CharField(max_length=100, blank=True, null=True)
	links = models.CharField(max_length=100, blank=True, null=True)
	about= models.CharField(max_length=100, blank=True, null=True)
	active= models.BooleanField(default=1)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE, related_name="companyinfo_created_by")
	updated_by = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE, related_name="companyinfo_updated_by")

	class Meta:
		db_table="CompanyInfo"

class UserCompanyRole(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE)
	company = models.ForeignKey(Company,blank=False, null=False,on_delete=models.CASCADE)
	role = models.ForeignKey(Roles,blank=False, null=False,on_delete=models.CASCADE)
	isActive = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE, related_name="user_role_created_by")
	updated_at = models.DateTimeField(auto_now=True)
	updated_by = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE, related_name="user_role_updated_by")

	class Meta:
		db_table="UserCompanyRole"

@receiver(post_save,sender=Company)
def save_company_info(sender,instance,created,*args, **kwargs):
	try:
		# logging.info("try==>{}".format(created))
		if created:
			getCompanyInfo=CompanyInfo.objects.filter(company=instance)
			if len(getCompanyInfo)==0:
				getCompanyInfo=CompanyInfo.objects.create(company=instance
											,created_by=instance.created_by
											,updated_by=instance.updated_by)
			elif instance.active==False:
				getCompanyInfo.active=False
				getCompanyInfo=getCompanyInfo[0]
				getCompanyInfo.updated_by=instance.created_by
				getCompanyInfo.save()
	except Exception as e:
		logging.info("exceptoin==>{}".format(e))
		pass 
	
	