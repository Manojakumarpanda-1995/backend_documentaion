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
		data={"email":"su1@momenttext.com","password":"Password@123"}
		response=client.post(request,data=json.dumps(data)
							 ,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["token"]==Users.objects.get(id=1).token
		assert response["name"]=="backend Super User 1"
		assert response["email"]=="su1@momenttext.com"
		assert response["company_id"]== 1
		assert response["role"]=="SUPER-USER"
		
	def test_login_with_invalid_data(self,client):
		
		request=reverse("usermanagement:loginapi")
		data={"email":"su1@momenttext.com","password":"Password@12343"}
		response=client.post(request,data=json.dumps(data)
							 ,content_type="application/json")
		assert response.status_code==200
		user=Users.objects.get(email=data["email"])
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="The username or password is not correct"
		curr_access=AccessManagement.objects.get(name=user)
		assert curr_access.password_attempts == 1
		
	def test_login_with_invalid_email(self,client):
		
		request=reverse("usermanagement:loginapi")
		data={"email":"su1@gmail.com","password":"Password@123"}
		response=client.post(request,data=json.dumps(data)
							 ,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Invalid Email."

	def test_login_with_missing_data(self,client):
		
		request=reverse("usermanagement:loginapi")
		data={"email":"su1@gmail.com","passwords":"Password@123"}
		response=client.post(request,data=json.dumps(data)
							 ,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="The username or password is not correct"

	@pytest.mark.parametrize("email,password",[
		("testuser1@momenttext.com","Password@123"),("testuser2@momenttext.com","Password@123")
		,("testuser3@momenttext.com","Password@123"),
		("testuser4@momenttext.com","Password@123"),("testuser5@momenttext.com","Password@123")
		,("testuser6@momenttext.com","Password@123"),
		("testuser7@momenttext.com","Password@123"),("testuser8@momenttext.com","Password@123")
		])	 
	def test_login_with_multiple_invalid_attempt(self,client,
                        email,password,setup_multiple_invalid):
		
		request=reverse("usermanagement:loginapi")
		data={"email":email,"password":password}
		response=client.post(request,data=json.dumps(data),content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["message"] == "Multiple invalid password attempts. Please try after sometime"
		assert response["statuscode"] == 400
	
	@pytest.mark.parametrize("email,password",[
		("testuser1@momenttext.com","Password@1234"),("testuser2@momenttext.com","Password@1234")
		,("testuser3@momenttext.com","Password@1234"),
		("testuser4@momenttext.com","Password@1234"),("testuser5@momenttext.com","Password@1234")
		,("testuser6@momenttext.com","Password@1234"),
		("testuser7@momenttext.com","Password@1234"),("testuser8@momenttext.com","Password@1234")
		])	 
	def test_login_with_attempt_pass_update(self,client,
                        email,password,setup_invalid_attempt_update):
		
		request=reverse("usermanagement:loginapi")
		data={"email":email,"password":password}
		getAccess=AccessManagement.objects.filter(name__email=email)[0]
		count=getAccess.password_attempts
		response=client.post(request,data=json.dumps(data),content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["message"] == "The username or password is not correct"
		assert response["statuscode"] == 400
		getAccess=AccessManagement.objects.filter(name__email=email)[0]
		assert getAccess.last_login_attempt is not None
		assert getAccess.password_attempts==count-1
	
	@pytest.mark.parametrize("email,password",[
		("testuser1@momenttext.com","Password@1234"),("testuser2@momenttext.com","Password@1234")
		,("testuser3@momenttext.com","Password@1234"),
		("testuser4@momenttext.com","Password@1234"),("testuser5@momenttext.com","Password@1234")
		,("testuser6@momenttext.com","Password@1234"),
		("testuser7@momenttext.com","Password@1234"),("testuser8@momenttext.com","Password@1234")
		])	 
	def test_login_with_invalid_first_attempt(self,client,
                        email,password,setup_invalid_first_attempt):
		
		request=reverse("usermanagement:loginapi")
		data={"email":email,"password":password}
		response=client.post(request,data=json.dumps(data),content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["message"] == "The username or password is not correct"
		assert response["statuscode"] == 400
		getAccess=AccessManagement.objects.filter(name__email=email)[0]
		assert getAccess.last_login_attempt is not None
		assert getAccess.password_attempts==1

	@pytest.mark.parametrize("email,password",[
		("testuser4@momenttext.com","Password@123"),("testuser5@momenttext.com","Password@123")
		,("testuser6@momenttext.com","Password@123")
		])	 
	def test_login_without_authorization(self,client,
                        email,password,setup_saved_user):
		
		request=reverse("usermanagement:loginapi")
		data={"email":email,"password":password}
		response=client.post(request,data=json.dumps(data),content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"] == 400
		assert response["message"] =="You are not authorized to login. Please contact the administrator."
  
	@pytest.mark.parametrize("email,password",[
		("testuser1@momenttext.com","Password@123"),("testuser2@momenttext.com","Password@123")
		,("testuser3@momenttext.com","Password@123"),
		("testuser4@momenttext.com","Password@123"),("testuser5@momenttext.com","Password@123")
		,("testuser6@momenttext.com","Password@123"),
		("testuser7@momenttext.com","Password@123"),("testuser8@momenttext.com","Password@123")
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
		response=response.json()
		assert response["statuscode"] == 400
		getAccess=AccessManagement.objects.filter(name__email=email)[0]
		assert getAccess.last_login_attempt is None
		assert getAccess.password_attempts ==0

	@pytest.mark.parametrize("email,password",[
		("testuser1@momenttext.com","Password@1234"),("testuser2@momenttext.com","Password@1234")
		,("testuser3@momenttext.com","Password@1234"),
		("testuser4@momenttext.com","Password@1234"),("testuser5@momenttext.com","Password@1234")
		,("testuser6@momenttext.com","Password@1234"),
		("testuser7@momenttext.com","Password@1234"),("testuser8@momenttext.com","Password@1234")
		])	 
	def test_login_with_wrong_password(self,client,
                        email,password,setup_saved_user):
		
		request=reverse("usermanagement:loginapi")
		data={"email":email,"password":password}
		response=client.post(request,data=json.dumps(data),content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"] == 400
		assert response["message"] == "The username or password is not correct"
		getAccess=AccessManagement.objects.filter(name__email=email)[0]
		assert getAccess.last_login_attempt is not None
		assert getAccess.password_attempts ==1
	
	@pytest.mark.parametrize("email,password",[
		("testuser1@momenttext.com","Password@123"),("testuser2@momenttext.com","Password@123")
		,("testuser3@momenttext.com","Password@123"),
		("testuser7@momenttext.com","Password@123"),("testuser8@momenttext.com","Password@123")
		])	 
	def test_login_without_verification(self,client,
                        email,password,setup_multiple_invalid_reset):
		
		request=reverse("usermanagement:loginapi")
		data={"email":email,"password":password}
		response=client.post(request,data=json.dumps(data),content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"] == 400
		assert response["message"] == "Your account is not active. Please click on the link sent to your email at the time of Registration."

class Test_reset_password():
    
	@pytest.mark.parametrize("email",[("testuser1@momenttext.com"),
		("testuser4@momenttext.com"),("testuser2@momenttext.com"),
		("testuser6@momenttext.com")
		,("testuser3@momenttext.com"),("testuser5@momenttext.com"),
		("testuser7@momenttext.com"),("testuser8@momenttext.com")
		])	 
	def test_reset_password_with_valid_data(self,client,email,setup_saved_user):
		request=reverse("usermanagement:reset-password")
		data=json.dumps({"email":email})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["message"]=="OTP to email ID {} sent successfully.".format(email)

	@pytest.mark.parametrize("email",[("testuser1@momenttext.com"),
		("testuser4@momenttext.com"),("testuser2@momenttext.com")
		,("testuser3@momenttext.com")
		])	 
	def test_reset_password_without_access_management(self,client,email,setup_user_without_access):
		request=reverse("usermanagement:reset-password")
		data=json.dumps({"email":email})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		# print("assert ==>",response["message"])
		assert response["message"]=="User Access for email {} does not exists in the database.".format(email)

	@pytest.mark.parametrize("email",[("testuser1@gmail.com"),
		("testuser4@gmail.com"),("testuser2@gmail.com"),("testuser6@gmail.com")
		,("testuser3@gmail.com"),("testuser5@gmail.com"),
		("testuser7@gmail.com"),("testuser8@gmail.com")
		])	 
	def test_reset_password_with_invalid_email(self,client,email,setup_saved_user):
		request=reverse("usermanagement:reset-password")
		data=json.dumps({"email":email})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Email ID {} does not exists in the database.".format(email)

	@pytest.mark.parametrize("email",[
		("testuser1@momenttext.com"),("testuser2@momenttext.com")
		,("testuser3@momenttext.com"),("testuser4@momenttext.com")
		])	 
	def test_reset_password_with_multiple_invalid_attempt(self,client,
                        email,setup_multiple_invalid_for_pass_reset):
		request=reverse("usermanagement:reset-password")
		data=json.dumps({"email":email})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["message"] == "Multiple password requests for email ID {} received. Please try after sometime.".format(email)
		assert response["statuscode"] == 400
  
	@pytest.mark.parametrize("email",[
		("testuser5@momenttext.com"),("testuser6@momenttext.com")
		,("testuser7@momenttext.com"),("testuser8@momenttext.com")
		])	 
	def test_reset_password_with_multiple_invalid_attempt_reset(self,client,
                        email,setup_multiple_invalid_for_pass_reset):
		request=reverse("usermanagement:reset-password")
		data=json.dumps({"email":email})
		getAccess=AccessManagement.objects.get(name__email=email)
		assert getAccess.last_password_reset_request is not None
		assert getAccess.password_reset_request_count == count_threshold
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		getAccess=AccessManagement.objects.get(name__email=email)
		assert getAccess.password_reset_request_count == 0
		assert response["message"] == "OTP to email ID {} sent successfully.".format(email)
		assert response["statuscode"] == 200

	@pytest.mark.parametrize("email",[
		("testuser1@momenttext.com"),("testuser2@momenttext.com")
		,("testuser3@momenttext.com"),("testuser4@momenttext.com")
		])	 
	def test_reset_password_counter_increment(self,client,
                        email,setup_update_password_access_counter):
		request=reverse("usermanagement:reset-password")
		data=json.dumps({"email":email})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		getAccess=AccessManagement.objects.get(name__email=email)
		assert getAccess.last_password_reset_request is not None
		assert getAccess.password_reset_request_count == 3
		assert response["message"] == "OTP to email ID {} sent successfully.".format(email)
		assert response["statuscode"] == 200
  
	@pytest.mark.parametrize("email",[
		("testuser5@momenttext.com"),("testuser6@momenttext.com")
		,("testuser7@momenttext.com"),("testuser8@momenttext.com")
		])	 
	def test_reset_password_counter_reset(self,client,
                        email,setup_update_password_access_counter):
		request=reverse("usermanagement:reset-password")
		data=json.dumps({"email":email})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		getAccess=AccessManagement.objects.get(name__email=email)
		assert getAccess.last_password_reset_request is not None
		assert getAccess.password_reset_request_count == 0
		assert response["message"] == "OTP to email ID {} sent successfully.".format(email)
		assert response["statuscode"] == 200
	
	@pytest.mark.parametrize("email",[
		("testuser5@momenttext.com"),("testuser6@momenttext.com")
		,("testuser7@momenttext.com"),("testuser8@momenttext.com")
		])	 
	def test_reset_password_with_missing_data(self,client,
                        email,setup_update_password_access_counter):
		request=reverse("usermanagement:reset-password")
		data=json.dumps({"emails":email})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"] == 500
                
class Test_update_password():
    
	@pytest.mark.parametrize("email,password,otp",[
		("testuser1@momenttext.com","Password@1235445323","4yT28GN7")
		,("testuser2@momenttext.com","Password@123545jkw","4yT28GN7")
		,("testuser3@momenttext.com","Password@123545jkw","4yT28GN7")
		,("testuser4@momenttext.com","Password@123545jkw","4yT28GN7")
		])	
	def test_update_password_with_valid_data(self,client,email
								,password,otp,setup_update_password):
		request=reverse("usermanagement:update-password")
		token=Users.objects.get(email=email).token
		data=json.dumps({"email":email,"new_password":password,"otp":otp})
		getAccess=AccessManagement.objects.get(name__email=email)
		assert getAccess.otp is not None
		assert getAccess.otp_attempts == 2
		assert getAccess.otp_expiry_time is not None
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		getAccess=AccessManagement.objects.get(name__email=email)
		assert getAccess.last_otp_attempt is None
		assert getAccess.otp is None
		assert getAccess.otp_attempts ==0
		assert getAccess.otp_expiry_time is None
		getUsers=Users.objects.get(email=email)
		assert getUsers.token !=token
		assert response["token"]==getUsers.token
		assert response["message"]=="Password changed successfully."
		assert response["statuscode"]==200

	@pytest.mark.parametrize("email,password,otp",[
		("testuser1@momenttext.com","Password@12354","4yT28GN7")
		,("testuser2@momenttext.com","Password@12354","4yT28GN7")
		,("testuser3@momenttext.com","Password@12354","4yT28GN7")
		,("testuser4@momenttext.com","Password@12354","4yT28GN7")
		,("testuser5@momenttext.com","Password@12354","4yT28GN7")
		,("testuser6@momenttext.com","Password@12354","4yT28GN7")
		,("testuser7@momenttext.com","Password@12354","4yT28GN7")
		,("testuser8@momenttext.com","Password@12354","4yT28GN7")
		])	
	def test_update_password_with_invalid_password_pattern(self,client,email
								,password,otp,setup_update_password):
		request=reverse("usermanagement:update-password")
		data=json.dumps({"email":email,"new_password":password,"otp":otp})
		response=client.post(request,data=data,content_type="application/json")
		response.status_code==200
		response=response.json()
		assert response["message"]=="Password entered for email ID {} does not meet the conditions.".format(email)
		assert response["statuscode"]==500

	@pytest.mark.parametrize("email,password,otp",[
		("testuser1@momenttext.com","Password@12354","4yT28GN7")
		,("testuser2@momenttext.com","Password@12354","4yT28GN7")
		,("testuser3@momenttext.com","Password@12354","4yT28GN7")
		,("testuser4@momenttext.com","Password@12354","4yT28GN7")
		])	 
	def test_update_password_without_access_management(self,client,email,password,otp,setup_user_without_access):
		request=reverse("usermanagement:update-password")
		data=json.dumps({"email":email,"new_password":password,"otp":otp})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
		assert response["message"]=="User Access for email {} does not exists in the database.".format(email)
	
	def test_update_password_with_missing_data(self,client,setup_user_without_access):
		request=reverse("usermanagement:update-password")
		data=json.dumps({"email":"testuser1@momenttext.com","password":"Password@1234567","otp":"4yT28GN7"})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
	
	@pytest.mark.parametrize("email,password,otp",[
		("testuser1@gmail.com","Password@12354","4yT28GN7")
		,("testuser2@gmail.com","Password@12354","4yT28GN7")
		,("testuser3@gmail.com","Password@12354","4yT28GN7")
		,("testuser4@gmail.com","Password@12354","4yT28GN7")
		])	 
	def test_update_password_with_invalid_email(self,client,email,password,otp,setup_saved_user):
		request=reverse("usermanagement:update-password")
		data=json.dumps({"email":email,"new_password":password,"otp":otp})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
		assert response["message"]=="Email ID {} does not exists in the database.".format(email)
	
	@pytest.mark.parametrize("email,password,otp",[
		("testuser1@momenttext.com","Password@12354jkj","4yT28GN7")
		,("testuser2@momenttext.com","Password@12354jkj","4yT28GN7")
		,("testuser3@momenttext.com","Password@12354jkj","4yT28GN7")
		,("testuser4@momenttext.com","Password@12354jkj","4yT28GN7")
		])	 
	def test_update_password_without_otp_generation(self,client,email,password,otp,setup_saved_user):
		request=reverse("usermanagement:update-password")
		data=json.dumps({"email":email,"new_password":password,"otp":otp})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
		assert response["message"]=="No OTP has been initiated for email ID {}.".format(email)
	
	@pytest.mark.parametrize("email,password,otp",[
		("testuser5@momenttext.com","Password@12354jkhd","4yT28GN7")
		,("testuser6@momenttext.com","Password@12354jkhd","4yT28GN7")
		,("testuser7@momenttext.com","Password@12354jkhd","4yT28GN7")
		,("testuser8@momenttext.com","Password@12354jkhd","4yT28GN7")
  		])
	def test_update_password_with_expired_otp(self,client,email,password,otp,setup_update_password):
		request=reverse("usermanagement:update-password")
		data=json.dumps({"email":email,"new_password":password,"otp":otp})
		getAccess=AccessManagement.objects.get(name__email=email)
		assert getAccess.otp is not None
		assert getAccess.otp_attempts == 2
		assert getAccess.otp_expiry_time is not None
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		getAccess=AccessManagement.objects.get(name__email=email)
		assert getAccess.last_otp_attempt is None
		assert getAccess.otp is None
		assert getAccess.otp_attempts == 0
		assert getAccess.otp_expiry_time is None
		assert response["statuscode"]==500
		assert response["message"]=="OTP expired for email ID {}.".format(email)
		
	@pytest.mark.parametrize("email,password,otp",[
		("testuser1@momenttext.com","Password@12354jkhd","yJgj1378")
		,("testuser2@momenttext.com","Password@12354jkhd","yJgj1378")
		,("testuser3@momenttext.com","Password@12354jkhd","yJgj1378")
		,("testuser4@momenttext.com","Password@12354jkhd","yJgj1378")
		])
	def test_update_password_with_invalid_otp(self,client,email,password,otp,setup_update_password):
		request=reverse("usermanagement:update-password")
		data=json.dumps({"email":email,"new_password":password,"otp":otp})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
		getAccess=AccessManagement.objects.get(name__email=email)
		assert response["message"]=="Incorrect OTP."
		assert getAccess.otp_attempts == 1
		
	@pytest.mark.parametrize("email,password,otp",[
		("testuser5@momenttext.com","Password@12354jkhd","4yT28GN7")
		,("testuser6@momenttext.com","Password@12354jkhd","4yT28GN7")
		,("testuser7@momenttext.com","Password@12354jkhd","4yT28GN7")
		,("testuser8@momenttext.com","Password@12354jkhd","4yT28GN7")
  		])
	def test_update_password_with_incorrect_otp_after_threshold(self,client
									,email,password,otp,setup_update_password_access_counter):
		request=reverse("usermanagement:update-password")
		data=json.dumps({"email":email,"new_password":password,"otp":otp})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		getAccess=AccessManagement.objects.get(name__email=email)
		assert getAccess.otp_attempts == 1
		assert response["statuscode"]==500
		assert response["message"]=="Incorrect OTP.".format(email)
		
	@pytest.mark.parametrize("email,password,otp",[
		("testuser1@momenttext.com","Password@12354jkhd","yJgj1378")
		,("testuser2@momenttext.com","Password@12354jkhd","yJgj1378")
		,("testuser3@momenttext.com","Password@12354jkhd","yJgj1378")
		,("testuser4@momenttext.com","Password@12354jkhd","yJgj1378")
		])
	def test_update_password_with_increase_otp_counter(self,client
							,email,password,otp,setup_update_password_access_counter):
		request=reverse("usermanagement:update-password")
		data=json.dumps({"email":email,"new_password":password,"otp":otp})
		getAccess=AccessManagement.objects.get(name__email=email)
		assert getAccess.otp_attempts == 4
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
		getAccess=AccessManagement.objects.get(name__email=email)
		assert response["message"]=="Incorrect OTP."
		assert getAccess.otp_attempts == 5
		
  
















































@pytest.mark.xfail        
class Test_new_password():
	def test_new_password(self,client):
		request=reverse("usermanagement:new-password")
@pytest.mark.xfail        
class Test_logout():
	def test_logout(self,client):
		request=reverse("usermanagement:logout")
@pytest.mark.xfail        
class Test_check_token():
	def test_check_token(self,client):
		request=reverse("usermanagement:check-token")
@pytest.mark.xfail       
class Test_download_file():
	def test_download_file(self,client):
		request=reverse("usermanagement:download-file")
@pytest.mark.xfail       
class Test_create_role():
	def test_create_role(self,client):
		request=reverse("usermanagement:create-role")
@pytest.mark.xfail        
class Test_get_role():
	def test_get_role(self,client):
		request=reverse("usermanagement:get-role")
@pytest.mark.xfail        
class Test_register_user():
	def test_register_user(self,client):
		request=reverse("usermanagement:register-user")
@pytest.mark.xfail    
class Test_register_worker():
	def test_register_worker(self,client):
		request=reverse("usermanagement:register-worker")
@pytest.mark.xfail        
class Test_register_access():
	def test_register_access(self,client):
		request=reverse("usermanagement:register-access-request")
@pytest.mark.xfail    
class Test_edit_user():
	def test_edit_user(self,client):
		request=reverse("usermanagement:edit-user")
@pytest.mark.xfail    
class Test_edit_user_byid():
	def test_edit_user_byid(self,client):
		request=reverse("usermanagement:edit-user-byid")
@pytest.mark.xfail    
class Test_deactivate_user():
	def test_deactivate_user(self,client):
		request=reverse("usermanagement:deactivate-user")
@pytest.mark.xfail        
class Test_list_user_byemail():
	def test_list_user_byemail(self,client):
		request=reverse("usermanagement:list-user-byemail")
        

	
  
  
  
  
  
  
  
  
  
  
  
  