import json

import pytest
from django import dispatch
# from usermanagement.utils.store_activity_logs import func_store_activity_logs
from django.conf import settings
from django.test.client import Client as client
from django.urls import reverse
from django.utils import timezone
from organization.models import *
from project.models import *
from usermanagement.models import *
from usermanagement.models import AccessManagement, Users
from usermanagement.utils.hash import (decryption, encryption,
									   generate_passwords)
from django.conf import settings
refresh_lockout = getattr(settings, "LOCKOUT_COUNT_RESET_DURATION", None)
time_threshold = getattr(settings, "INCORRECT_PASSWORD_COUNT_THRESHOLD", None)
count_threshold = getattr(settings, "INCORRECT_PASSWORD_COUNT_MAX_ATTEMPTS", None)
from faker import Faker

fake=Faker()

class Test_login():
	
	def test_login_with_valid_data(self,client):
		
		request=reverse("usermanagement:loginapi")
		data={"email":"su1@kpmg.com","password":"Password@123"}
		response=client.post(request,data=json.dumps(data)
							 ,content_type="application/json")
		assert response.status_code==200
		data = response.json()
		assert data["statuscode"]==200
		assert data["token"]==Users.objects.get(id=1).token
		assert data["name"]=="backend Super User 1"
		assert data["email"]=="su1@kpmg.com"
		assert data["company_id"]== 1
		assert data["role"]=="SUPER-USER"
		
	def test_login_with_invalid_data(self,client):
		
		request=reverse("usermanagement:loginapi")
		data={"email":"su1@kpmg.com","password":"Password@12343"}
		response=client.post(request,data=json.dumps(data)
							 ,content_type="application/json")
		assert response.status_code==200
		user=Users.objects.get(email=data["email"])
		data = response.json()
		assert data["statuscode"]==400
		assert data["message"]=="The username or password is not correct"
		curr_access=AccessManagement.objects.get(name=user)
		assert curr_access.password_attempts == 1
		
	def test_login_with_invalid_email(self,client):
		
		request=reverse("usermanagement:loginapi")
		data={"email":"su1@gmail.com","password":"Password@123"}
		response=client.post(request,data=json.dumps(data)
							 ,content_type="application/json")
		assert response.status_code==200
		data = response.json()
		assert data["statuscode"]==400
		assert data["message"]=="Invalid Email."

	def test_login_with_missing_data(self,client):
		
		request=reverse("usermanagement:loginapi")
		data={"email":"su1@gmail.com","passwords":"Password@123"}
		response=client.post(request,data=json.dumps(data)
							 ,content_type="application/json")
		assert response.status_code==200
		data = response.json()
		assert data["statuscode"]==400
		assert data["message"]=="The username or password is not correct"

	@pytest.mark.parametrize("email,password",[
		("testuser1@kpmg.com","Password@123"),("testuser2@kpmg.com","Password@123")
		,("testuser3@kpmg.com","Password@123"),
		("testuser4@kpmg.com","Password@123"),("testuser5@kpmg.com","Password@123")
		,("testuser6@kpmg.com","Password@123"),
		("testuser7@kpmg.com","Password@123"),("testuser8@kpmg.com","Password@123")
		])	 
	def test_login_with_multiple_invalid_attempt(self,client,
                        email,password,setup_multiple_invalid):
		
		request=reverse("usermanagement:loginapi")
		data={"email":email,"password":password}
		response=client.post(request,data=json.dumps(data),content_type="application/json")
		assert response.status_code==200
		data=response.json()
		assert data["message"] == "Multiple invalid password attempts. Please try after sometime"
		assert data["statuscode"] == 400
	
	@pytest.mark.parametrize("email,password",[
		("testuser1@kpmg.com","Password@1234"),("testuser2@kpmg.com","Password@1234")
		,("testuser3@kpmg.com","Password@1234"),
		("testuser4@kpmg.com","Password@1234"),("testuser5@kpmg.com","Password@1234")
		,("testuser6@kpmg.com","Password@1234"),
		("testuser7@kpmg.com","Password@1234"),("testuser8@kpmg.com","Password@1234")
		])	 
	def test_login_with_attempt_pass_update(self,client,
                        email,password,setup_invalid_attempt_update):
		
		request=reverse("usermanagement:loginapi")
		data={"email":email,"password":password}
		getAccess=AccessManagement.objects.filter(name__email=email)[0]
		count=getAccess.password_attempts
		response=client.post(request,data=json.dumps(data),content_type="application/json")
		assert response.status_code==200
		data=response.json()
		assert data["message"] == "The username or password is not correct"
		assert data["statuscode"] == 400
		getAccess=AccessManagement.objects.filter(name__email=email)[0]
		assert getAccess.last_login_attempt is not None
		assert getAccess.password_attempts==count-1
	
	@pytest.mark.parametrize("email,password",[
		("testuser1@kpmg.com","Password@1234"),("testuser2@kpmg.com","Password@1234")
		,("testuser3@kpmg.com","Password@1234"),
		("testuser4@kpmg.com","Password@1234"),("testuser5@kpmg.com","Password@1234")
		,("testuser6@kpmg.com","Password@1234"),
		("testuser7@kpmg.com","Password@1234"),("testuser8@kpmg.com","Password@1234")
		])	 
	def test_login_with_invalid_first_attempt(self,client,
                        email,password,setup_invalid_first_attempt):
		
		request=reverse("usermanagement:loginapi")
		data={"email":email,"password":password}
		response=client.post(request,data=json.dumps(data),content_type="application/json")
		assert response.status_code==200
		data=response.json()
		assert data["message"] == "The username or password is not correct"
		assert data["statuscode"] == 400
		getAccess=AccessManagement.objects.filter(name__email=email)[0]
		assert getAccess.last_login_attempt is not None
		assert getAccess.password_attempts==1

	@pytest.mark.parametrize("email,password",[
		("testuser4@kpmg.com","Password@123"),("testuser5@kpmg.com","Password@123")
		,("testuser6@kpmg.com","Password@123")
		])	 
	def test_login_without_authorization(self,client,
                        email,password,setup_saved_user):
		
		request=reverse("usermanagement:loginapi")
		data={"email":email,"password":password}
		response=client.post(request,data=json.dumps(data),content_type="application/json")
		assert response.status_code==200
		data=response.json()
		assert data["statuscode"] == 400
		assert data["message"] =="You are not authorized to login. Please contact the administrator."
  
	@pytest.mark.parametrize("email,password",[
		("testuser1@kpmg.com","Password@123"),("testuser2@kpmg.com","Password@123")
		,("testuser3@kpmg.com","Password@123"),
		("testuser4@kpmg.com","Password@123"),("testuser5@kpmg.com","Password@123")
		,("testuser6@kpmg.com","Password@123"),
		("testuser7@kpmg.com","Password@123"),("testuser8@kpmg.com","Password@123")
		])	 
	def test_login_with_invalid_attempt_reset(self,client,
                        email,password,setup_multiple_invalid_reset):
		
		request=reverse("usermanagement:loginapi")
		data={"email":email,"password":password}
		getAccess=AccessManagement.objects.filter(name__email=email)[0]
		assert getAccess.last_login_attempt is not None
		assert getAccess.password_attempts==count_threshold
		response=client.post(request,data=json.dumps(data),content_type="application/json")
		assert response.status_code==200
		data=response.json()
		assert data["statuscode"] == 400
		getAccess=AccessManagement.objects.filter(name__email=email)[0]
		assert getAccess.last_login_attempt is None
		assert getAccess.password_attempts ==0

	@pytest.mark.parametrize("email,password",[
		("testuser1@kpmg.com","Password@1234"),("testuser2@kpmg.com","Password@1234")
		,("testuser3@kpmg.com","Password@1234"),
		("testuser4@kpmg.com","Password@1234"),("testuser5@kpmg.com","Password@1234")
		,("testuser6@kpmg.com","Password@1234"),
		("testuser7@kpmg.com","Password@1234"),("testuser8@kpmg.com","Password@1234")
		])	 
	def test_login_with_wrong_password(self,client,
                        email,password,setup_saved_user):
		
		request=reverse("usermanagement:loginapi")
		data={"email":email,"password":password}
		response=client.post(request,data=json.dumps(data),content_type="application/json")
		assert response.status_code==200
		data=response.json()
		assert data["statuscode"] == 400
		assert data["message"] == "The username or password is not correct"
		getAccess=AccessManagement.objects.filter(name__email=email)[0]
		assert getAccess.last_login_attempt is not None
		assert getAccess.password_attempts ==1
	
	@pytest.mark.parametrize("email,password",[
		("testuser1@kpmg.com","Password@123"),("testuser2@kpmg.com","Password@123")
		,("testuser3@kpmg.com","Password@123"),
		("testuser7@kpmg.com","Password@123"),("testuser8@kpmg.com","Password@123")
		])	 
	def test_login_without_verification(self,client,
                        email,password,setup_multiple_invalid_reset):
		
		request=reverse("usermanagement:loginapi")
		data={"email":email,"password":password}
		response=client.post(request,data=json.dumps(data),content_type="application/json")
		assert response.status_code==200
		data=response.json()
		assert data["statuscode"] == 400
		assert data["message"] == "Your account is not active. Please click on the link sent to your email at the time of Registration."


	
  
  
  
  
  
  
  
  
  
  
  
  