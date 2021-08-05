from django.db import models
from django.core.validators import validate_email
from usermanagement.models import Users, Roles


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