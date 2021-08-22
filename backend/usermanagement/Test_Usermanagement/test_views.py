import json
import string
import random
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
	
	#This is for request with all valid information
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
  
	#This is for request with all valid information
	@pytest.mark.parametrize("email,password,role,name",[
		("companyadmin@momenttext.com","Password@1234567","COMPANY-ADMIN","Company Admin")
		# ,("projectadmin@momenttext.com","Password@1237654","PROJECT-ADMIN","Project Admin")
		# ,("projectadmin@momenttext.com","Password@1237654","PROJECT-ADMIN","Project Admin")
		# ,("testuser@momenttext.com","Password@1232424","USER","Test User")
		# ,("user@momenttext.com","Password@1231212","USER","End User")
		])
	def test_login_with_valid_users(self,client,email,password,role,name):
		
		request=reverse("usermanagement:loginapi")
		data={"email":email,"password":password}
		response=client.post(request,data=json.dumps(data)
							 ,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["token"]==Users.objects.get(email=email).token
		assert response["name"]==name
		assert response["email"]==email
		assert response["company_id"]== 2
		assert response["role"]==role

	#Test case with wrong password		
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
		getAccess=AccessManagement.objects.get(name=user)
		assert getAccess.password_attempts == 1

	#Test case with a wrong email that is not exist in database	
	def test_login_with_invalid_email(self,client):
		
		request=reverse("usermanagement:loginapi")
		data={"email":"su1@gmail.com","password":"Password@123"}
		response=client.post(request,data=json.dumps(data)
							 ,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Invalid Email."

	#Test case with invalid/missing parameters in request
	def test_login_with_missing_data(self,client):
		
		request=reverse("usermanagement:loginapi")
		data={"email":"su1@gmail.com","passwords":"Password@123"}
		response=client.post(request,data=json.dumps(data)
							 ,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="The username or password is not correct"

	#Test case for users already attempted multiple time with wrong username or password
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

	# Test case to verify that the password_attempt counter is updating or not after wrong password entered	
	@pytest.mark.parametrize("email,password",[
		("testuser1@momenttext.com","Password@12341"),("testuser2@momenttext.com","Password@12343")
		,("testuser3@momenttext.com","Password@12342"),
		("testuser4@momenttext.com","Password@1234a"),("testuser5@momenttext.com","Password@1234f")
		,("testuser6@momenttext.com","Password@1234t"),
		("testuser7@momenttext.com","Password@1234e"),("testuser8@momenttext.com","Password@1234y")
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

	# Test case to verify that the password_attempt counter after fist wrong attempt	
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

	#Test cases for user don"t login access
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

	#To check all the counter in access management are updating or not after successfully logedin.
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

	#Testing the attempt with wrong password
	@pytest.mark.parametrize("email,password",[
		("testuser1@momenttext.com","Password@1234rd"),("testuser2@momenttext.com","Password@123434")
		,("testuser3@momenttext.com","Password@1234df"),
		("testuser4@momenttext.com","Password@1234te"),("testuser5@momenttext.com","Password@1234cd")
		,("testuser6@momenttext.com","Password@1234df"),
		("testuser7@momenttext.com","Password@1234fs"),("testuser8@momenttext.com","Password@1234hr")
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

	#Testing users attempting for login without user verified.	
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
    #Test cases with all valid informations
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

	#Test case for users without access management 
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
		assert response["message"]=="User Access for email {} does not exists in the database.".format(email)

	#Test cases with invalid email emails of user
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

	#Test case for users already attempted multiple time with wrong username or password 
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

	#Test case to reset the multiple wrong username or password attempt to its original  
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

	#Test case with incorrect otp to check if the otp_attempts counter increasing or not
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

	#Test case to check the reset reset_password_request count   
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

	#Test case with missing/wrong request parameters	
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
    
	#Test cases with all valid information
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

	#Test cases with wrong password pattern
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
		assert response.status_code==200
		response=response.json()
		assert response["message"]=="Password entered for email ID {} does not meet the conditions.".format(email)
		assert response["statuscode"]==500

	#Test case for users without AccessManagement
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

	#Test case with request having missing/wrong parameter	
	def test_update_password_with_missing_data(self,client,setup_user_without_access):
		request=reverse("usermanagement:update-password")
		data=json.dumps({"email":"testuser1@momenttext.com","password":"Password@1234567","otp":"4yT28GN7"})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500

	#Test case with request having wrong email 	
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

	#Test case without the otp being generated for the user	
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

	#Test cases with expired otp 	
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

	#Test case with invalid otp in the request parameter		
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

	#Test case for sending incorrect otp after threshold time passed		
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
	
	#Test case with incorrect otp to check if the otp_attempts counter increasing or not		
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
		      
class Test_new_password():
	#Test cases with all valid information
	@pytest.mark.parametrize("email,password,new_pass",[
		("testuser1@momenttext.com","Password@123","newPassword@12345")
		,("testuser2@momenttext.com","Password@123","newPassword@12346")
		,("testuser3@momenttext.com","Password@123","newPassword@12347")
		,("testuser4@momenttext.com","Password@123","newPassword@12348")
		])	
	def test_new_password_with_valid_data(self,client
    				,email,password,new_pass,setup_user_for_new_password):
		request=reverse("usermanagement:new-password")
		data=json.dumps({"email":email,"old_password":password,"new_password":new_pass})
		getUser=Users.objects.get(email=email)
		assert getUser.password	==generate_passwords(password)			
		headers={"HTTP_AUTHORIZATION":getUser.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200	
		assert response["message"]=="Password changed successfully."
		getUser=Users.objects.get(email=email)
		assert getUser.password	==generate_passwords(new_pass)			
	
 	#Test cases for request with wrong old passwords
	@pytest.mark.parametrize("email,password,new_pass",[
		("testuser4@momenttext.com","Password@12344","newPassword@1234")
		,("testuser5@momenttext.com","Password@12332","newPassword@1234")
		,("testuser6@momenttext.com","Password@12312","newPassword@1234")
		,("testuser7@momenttext.com","Password@123jf","newPassword@1234")
		,("testuser8@momenttext.com","Password@123jf","newPassword@1234")
		])	
	def test_new_password_with_wrong_password(self,client
    				,email,password,new_pass,setup_user_for_new_password):
		request=reverse("usermanagement:new-password")
		data=json.dumps({"email":email,"old_password":password,"new_password":new_pass})
		getUser=Users.objects.get(email=email)			
		headers={"HTTP_AUTHORIZATION":getUser.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400	
		assert response["message"]=="Old Password is Incorrect."
	
	#Test cases for request with invalid token		 
	@pytest.mark.parametrize("email,password,new_pass",[
		("testuser5@momenttext.com","Password@123","newPassword@1234")
		])
	def test_new_password_with_invalid_token(self,client
    				,email,password,new_pass,setup_user_for_new_password):
		request=reverse("usermanagement:new-password")
		data=json.dumps({"email":"test_user","old_password":password,"new_password":new_pass})
		token=fake.uuid4()			
		headers={"HTTP_AUTHORIZATION":token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==403

	#Test cases for request with missing/wrong keys in data
	def test_new_password_with_missing_data(self,client,setup_saved_user):
		request=reverse("usermanagement:new-password")
		data=json.dumps({"email":"testuser5@momenttext.com","old_password":"Password@123"
        		,"new_passwords":"newPassword@1234"})
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email="testuser5@momenttext.com")}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
          
class Test_logout():
	#Test cases with all valid information
	@pytest.mark.parametrize("email",[("testuser1@momenttext.com")
		,("testuser3@momenttext.com"),("testuser5@momenttext.com"),
		("testuser7@momenttext.com"),("testuser8@momenttext.com")
		])	 
	def test_logout_with_valid_data(self,client,email,setup_saved_user):
		request=reverse("usermanagement:logout")
		data=json.dumps({"email":email})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["message"]=="User logged out successfully."

    #Test cases with wrong email valid information
	@pytest.mark.parametrize("email",[("testuser1@gmail.com"),
		("testuser4@gmail.com"),("testuser2@gmail.com"),
		("testuser6@gmail.com")
		])	 
	def test_logout_with_wrong_email(self,client,email,setup_saved_user):
		request=reverse("usermanagement:logout")
		data=json.dumps({"email":email})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Invalid token."
        
class Test_check_token():

	#Testing check token with all valid info
	def test_check_token_with_valid_data(self,client,setup_superusers):
		request=reverse("usermanagement:check-token")
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email="su1@momenttext.com").token}
		response=client.post(request,data=json.dumps({}),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["isUser"]==True
		assert response["role"]=="SUPER-USER"
		assert response["statuscode"]==200
  
	#Test cases for request with invalid token		 
	def test_check_token_with_invalid_token(self,client):
		request=reverse("usermanagement:check-token")
		data=json.dumps({})
		token=fake.uuid4()			
		headers={"HTTP_AUTHORIZATION":token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==403

	#Test cases for users whose roles are not assigned	 
	@pytest.mark.parametrize("email",[("testuser1@momenttext.com")
		,("testuser3@momenttext.com"),("testuser5@momenttext.com"),
		("testuser7@momenttext.com"),("testuser8@momenttext.com")
		])
	def test_check_token_without_role_assigned(self,client,email
                                            ,setup_user_for_new_password):
		request=reverse("usermanagement:check-token")
		data=json.dumps({})
		token=Users.objects.get(email=email).token			
		headers={"HTTP_AUTHORIZATION":token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==203
		assert response["isUser"]==False
       
class Test_create_role():
    #Test case for create role api with all valid information
	def test_create_role_with_valid_data(self,client):
		request=reverse("usermanagement:create-role")
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email="su1@momenttext.com").token}
		data=json.dumps({"role_name":"Group-Admin"})
		getRole=Roles.objects.count()
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["data"]==getRole+1
		assert response["message"]=="Role created successfully."
		assert response["statuscode"]==200

    #Test case for create role api with already existing role
	@pytest.mark.parametrize("role",[("Super-User"),("Company-Admin")
                                  ,("Project-Admin"),("user")
                                  ])
	def test_create_role_with_existing_role(self,client,role):
		request=reverse("usermanagement:create-role")
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email="su1@momenttext.com").token}
		data=json.dumps({"role_name":role})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["message"]=="Role already existed."
		assert response["statuscode"]==400
  
	#Test cases for request with invalid token		 
	def test_create_role_with_invalid_token(self,client):
		request=reverse("usermanagement:create-role")
		data=json.dumps({"role_name":"End-User"})
		token=fake.uuid4()			
		headers={"HTTP_AUTHORIZATION":token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==403
    
	#Test cases with users not authorized to create a role 
	@pytest.mark.parametrize("email",[
		("companyadmin@momenttext.com")
		,("projectadmin@momenttext.com")
		,("testuser@momenttext.com")
		,("user@momenttext.com")
		])
	def test_create_role(self,client,email):
		request=reverse("usermanagement:create-role")
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email=email).token}
		data=json.dumps({"role_name":"END-USER"})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["message"]=="Only SuperUser can create the role."
		assert response["statuscode"]==400

	#Test cases with missing/invalid request parameters
	def test_create_role_with_missing_data(self,client):
		request=reverse("usermanagement:create-role")
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email="su1@momenttext.com").token}
		data=json.dumps({"role_names":"END-USER"})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
        
class Test_get_role():
    #Test case for create role api with all valid information
	def test_get_role_with_valid_data(self,client):
		request=reverse("usermanagement:get-role")
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email="su1@momenttext.com").token}
		data=json.dumps({"role_name":"Super-User"})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["data"]["id"]==1
		assert response["data"]["role_name"]=="SUPER-USER"
		assert response["message"]=="Roles listed successfully."
		assert response["statuscode"]==200

    #Test case for create role api with already existing role
	@pytest.mark.parametrize("role,id",[("Super-User","1"),("Company-Admin","2")
                                  ,("Project-Admin","3"),("user","4")
                                  ])
	def test_get_role_with_existing_role(self,client,role,id):
		request=reverse("usermanagement:get-role")
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email="su1@momenttext.com").token}
		data=json.dumps({"role_name":role})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["message"]=="Roles listed successfully."
		assert response["statuscode"]==200
		assert response["data"]["id"]==int(id)
		assert response["data"]["role_name"]==role.upper()
  
	#Test cases for request with invalid token		 
	def test_get_role_with_invalid_token(self,client):
		request=reverse("usermanagement:get-role")
		data=json.dumps({"role_name":"End-User"})
		token=fake.uuid4()			
		headers={"HTTP_AUTHORIZATION":token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==403
    
	#Test cases with users not invalid role name 
	@pytest.mark.parametrize("email",[
		("companyadmin@momenttext.com")
		,("projectadmin@momenttext.com")
		,("testuser@momenttext.com")
		,("user@momenttext.com")
		])
	def test_get_role_with_invalid_role(self,client,email):
		request=reverse("usermanagement:get-role")
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email=email).token}
		data=json.dumps({"role_name":"END-USER"})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["message"]=="No role found in database."
		assert response["statuscode"]==400

	#Test cases with missing/invalid request parameters
	def test_get_role_with_missing_data(self,client):
		request=reverse("usermanagement:get-role")
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email="su1@momenttext.com").token}
		data=json.dumps({"role_names":"END-USER"})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500

	def test_get_role(self,client):
		request=reverse("usermanagement:get-role")
       
class Test_register_user():
    
    #Test case for register user api with all valid information
	def test_register_user_with_valid_data(self,client):
		request=reverse("usermanagement:register-user")
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email="su1@momenttext.com").token}
		data=json.dumps({"email":"testusers1@momenttext.com"
                   ,"first_name":"Test","last_name":"Users"
                   ,"name":"Test Users","designation":"Project-Admin"
                   ,"reporting_manager_id":1
                   ,"reporting_manager_email":"Rohit@momenttext.com"
                   ,"reporting_manager_name":"Rohit"})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["message"]=="User created successfully."
		assert response["statuscode"]==200

    #Test case for register user api with already existing users
	@pytest.mark.parametrize("email",[("companyadmin@momenttext.com")
			,("projectadmin@momenttext.com"),("testuser@momenttext.com")
            ,("user@momenttext.com")])
	def test_register_user_with_existing_user(self,client,email):
		request=reverse("usermanagement:register-user")
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email="su1@momenttext.com").token}
		data={"first_name":"Test","last_name":"Users"
                   ,"name":"Test Users","designation":"Project-Admin"
                   ,"reporting_manager_id":1
                   ,"reporting_manager_email":"Rohit@momenttext.com"
                   ,"reporting_manager_name":"Rohit"}
		data["email"]=email
		data=json.dumps(data)
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["message"]=="User already existed."
		assert response["statuscode"]==400
  
	#Test cases for request with invalid token		 
	def test_register_user_with_invalid_token(self,client):
		request=reverse("usermanagement:register-user")
		data=json.dumps({"role_name":"End-User"})
		token=fake.uuid4()			
		headers={"HTTP_AUTHORIZATION":token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Invalid Token."
    
	#Test cases with users not invalid role name 
	@pytest.mark.parametrize("email",[
		("company!admin1@momenttext.com")
		,("project#admin2@momenttext.com")
		,("project$admin4@momenttext.com")
		,("projectad&min5@momenttext.com")
		])
	def test_register_user_with_invalid_email(self,client,email):
		request=reverse("usermanagement:register-user")
		headers={"HTTP_AUTHORIZATION":Users.objects.get(id=1).token}
		data=json.dumps({"email":email
                   ,"first_name":"Test","last_name":"Users"
                   ,"name":"Test Users","designation":"Project-Admin"
                   ,"reporting_manager_id":1
                   ,"reporting_manager_email":"Rohit@momenttext.com"
                   ,"reporting_manager_name":"Rohit"})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["message"]=="Please try to add valid email."
		assert response["statuscode"]==400
  
	#Test cases with users having authorization to create except superuser 
	@pytest.mark.parametrize("email",[
		("companyadmin@momenttext.com")
		,("projectadmin@momenttext.com")
		])
	def test_register_user_with_all_authorized_user(self,client,email):
		request=reverse("usermanagement:register-user")
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email=email).token}
		data=json.dumps({"email":"testusers1@momenttext.com"
                   ,"first_name":"Test","last_name":"Users"
                   ,"name":"Test Users","designation":"Project-Admin"
                   ,"reporting_manager_id":1
                   ,"reporting_manager_email":"Rohit@momenttext.com"
                   ,"reporting_manager_name":"Rohit"})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["message"]=="User created successfully."
		assert response["statuscode"]==200

	#Test cases with missing/invalid request parameters
	def test_register_user_with_missing_data(self,client):
		request=reverse("usermanagement:register-user")
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email="su1@momenttext.com").token}
		data=json.dumps({"role_names":"END-USER"})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500

	#Test case for register	user without authorization	
	@pytest.mark.parametrize("email",[("testuser@momenttext.com")
                            ,("user@momenttext.com")])
	def test_register_user_without_authorization(self,client,email):
		request=reverse("usermanagement:register-user")
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email=email).token}
		data=json.dumps({"email":"testusers1@momenttext.com"
                   ,"first_name":"Test","last_name":"Users"
                   ,"name":"Test Users","designation":"Project-Admin"
                   ,"reporting_manager_id":1
                   ,"reporting_manager_email":"Rohit@momenttext.com"
                   ,"reporting_manager_name":"Rohit"})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["message"]=="You are not authorized to create user."
		assert response["statuscode"]==400
      
class Test_register_worker():
    
    #Test cases for register worker with all valid data
	def test_register_worker_with_valid_data(self,client):
		request=reverse("usermanagement:register-worker")
		data=json.dumps({"email":"Worker@email.com","name":"Worker",
				"phone_no":"9058908242","skill_sets":["Java","Python","c"]})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["message"]=="Workers registered successfully."
		assert response["data"] is not None
		assert response["statuscode"]==200

    #Test cases for register worker with existing users in Worker tables
	@pytest.mark.parametrize("email",[("Rohit@momenttext.com")])
	def test_register_worker_existing_worker(self,client,email,setup_register_worker):
		request=reverse("usermanagement:register-worker")
		data=json.dumps({"name":"Rohit","email":email
                   ,"phone_no":"987420937","skill_set":["jquery","json"]})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Workers already registered."
  
    #Test cases for register worker with invalid email format
	@pytest.mark.parametrize("email",[("roh#it@momenttext.com")
							,("ran!jit@momenttext.com")
							,("ron&it@momenttext.com")
							,("rob*in@momenttext.com")
							,("kart$#ik@momenttext.com")
                                   ])
	def test_register_worer_with_invalid_email(self,client,email,setup_register_worker):
		request=reverse("usermanagement:register-worker")
		data=json.dumps({"name":"Rohit","email":email
                   ,"phone_no":"987420937","skill_set":["jquery","json"]})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Please try to add valid email."
  
    #Test cases for register worker with existing users in Users tables
	@pytest.mark.parametrize("email",[
     	("testuser1@momenttext.com")
		,("testuser2@momenttext.com")
		,("testuser3@momenttext.com")
		,("testuser4@momenttext.com")])
	def test_register_worker_with_existing_user(self,client,email,setup_register_worker):
		request=reverse("usermanagement:register-worker")
		data=json.dumps({"name":"Rohit","email":email
                   ,"phone_no":"987420937","skill_set":["jquery","json"]})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Users with this email id's already exists. Try an another email."

	#Test cases of register worker api with missing parameters
	def test_register_worker_with_missing_parameter(self,client):
		request=reverse("usermanagement:register-worker")
		data=json.dumps({"email":"testuser@email.com"
                   ,"phone_no":"987420937","skill_set":["jquery","json"]})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Workers name can't be left blank."
  
	#Test cases of register worker api without email parameters
	def test_register_worker_without_email_parameter(self,client):
		request=reverse("usermanagement:register-worker")
		data=json.dumps({"name":fake.name()
                   ,"phone_no":"987420937","skill_set":["jquery","json"]})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
		       
class Test_register_access():

	#Test cases for register access request with all valid data
	def test_register_access_with_valid_data(self,client):
		request=reverse("usermanagement:register-access-request")
		data=json.dumps({"company_name":fake.company(),"name":"Jatin"
                   ,"email":"Jatin@momenttext.com"
			,"phone_number":"".join((random.choice(string.digits) for i in range(10)))
			,"skill_sets":["java","c++","jquery"]})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["message"]=="Access requests registered successfully."
		assert response["statuscode"]==200
		assert response["data"] is not None

	#Test cases for register access with existing users in Worker tables
	@pytest.mark.parametrize("email",[("Nitin@momenttext.com")])
	def test_register_access_request_existing_users(self,client,email
                        ,setup_register_access):
		request=reverse("usermanagement:register-access-request")
		data=json.dumps({"name":"Nitin","company_name":fake.company(),"email":email
                   ,"phone_no":"987420937","skill_set":["jquery","json"]})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Access requests with this email already registered."
  
    #Test cases for register access request with invalid email format
	@pytest.mark.parametrize("email",[("roh#it@momenttext.com")
							,("ran!jit@momenttext.com")
							,("ron&it@momenttext.com")
							,("rob*in@momenttext.com")
							,("kart$#ik@momenttext.com")
                                   ])
	def test_register_access_request_with_invalid_email(self,client,email):
		request=reverse("usermanagement:register-access-request")
		data=json.dumps({"company_name":fake.company(),"email":email
                   ,"phone_no":"987420937","skill_set":["jquery","json"]})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Please try to add valid email."
  
    #Test cases for register access request with existing users in Users tables
	@pytest.mark.parametrize("email",[
     	("testuser1@momenttext.com")
		,("testuser2@momenttext.com")
		,("testuser3@momenttext.com")
		,("testuser4@momenttext.com")
  		])
	def test_register_access_request_with_existing_user(self,client,email,setup_saved_user):
		request=reverse("usermanagement:register-access-request")
		data=json.dumps({"company_name":"Amazons","name":"Nitin","email":email
			,"phone_number":"".join((random.choice(string.digits) for i in range(10)))
			,"skill_sets":["java","c++","jquery"]})		
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Users with this email id's already exists. Try an another email."

	#Test cases of register access api with missing parameters
	def test_register_access_request_with_missing_parameter(self,client):
		request=reverse("usermanagement:register-access-request")
		data=json.dumps({"company_name":"TCS","email":"testuser@email.com"
                   ,"phone_no":"987420937","skill_set":["jquery","json"]})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
  
	#Test cases of register access request api without company name in parameters
	def test_register_access_request_without_company_name_parameter(self,client):
		request=reverse("usermanagement:register-access-request")
		data=json.dumps({"name":fake.name()
                   ,"phone_no":"987420937","skill_set":["jquery","json"]})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
		# assert response["message"]=="Access requests name can't be left blank."
		       
	#Test cases of register access request api with exsting company
	@pytest.mark.parametrize("name",[
		("Gmail")#,("Amazon"),("Tesla")
				#,("Infosys"),("Tata")
				])
	def test_register_access_request_with_existing_company(self,client,name,setup_company):
		request=reverse("usermanagement:register-access-request")
		data=json.dumps({"company_name":name,"name":"Nitin","email":fake.email(domain="momenttext.com")
			,"phone_number":"".join((random.choice(string.digits) for i in range(10)))
			,"skill_sets":["java","c++","jquery"]})
		response=client.post(request,data=data,content_type="application/json")
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Company with this name already registered. To claim contact with admin."
		       
@pytest.mark.xfail    
class Test_edit_user():
	def test_edit_user(self,client):
		request=reverse("usermanagement:edit-user")

































































@pytest.mark.xfail       
class Test_download_file():
	def test_download_file(self,client):
		request=reverse("usermanagement:download-file")
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
        

	
  
  
  
  
  
  
  
  
  
  
  
  