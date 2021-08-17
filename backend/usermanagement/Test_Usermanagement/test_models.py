import pytest
# from usermanagement.utils.store_activity_logs import func_store_activity_logs
from django.conf import settings
from django.utils import timezone
from organization.models import *
from project.models import *
from usermanagement.models import *
from usermanagement.models import AccessManagement, Users
from usermanagement.utils.hash import (decryption, encryption,
									   generate_passwords)


class Test_models():
	
	def test_users(self,setup_user):
		
		users=setup_user
		for obj in users:
			getUsers=Users.objects.create(**obj)
			getAccess=AccessManagement.objects.create(name=getUsers)
		
		assert Users.objects.count()==len(setup_user)+1
		getUsers=Users.objects.all()
		for x in range(len(users)):
			assert getUsers[0].email	== "su1@kpmg.com"
			assert getUsers[x+1].email	== users[x]["email"]
			assert getUsers[x+1].first_name == users[x]["first_name"]
			assert getUsers[x+1].last_name == users[x]["last_name"]
			assert getUsers[x+1].name == users[x]["name"]
			assert getUsers[x].password==generate_passwords("Password@123")
			assert getUsers[x].active==True
			assert getUsers[x].user_verified==True
			assert len(getUsers[x+1].hashkey)==10
			assert getUsers[x].reporting_manager_id==67890
			assert getUsers[x].reporting_manager_name=="Rohit Khandelwal"
			assert getUsers[x].reporting_manager_email=="Rohitkhandelwal@kpmg.com"
			assert len(getUsers)==AccessManagement.objects.count()
			
	def test_random_user(self,setup_random_user):	 
		users=setup_random_user
		for obj in users:
			getUsers=Users.objects.create(**obj)
			getAccess=AccessManagement.objects.create(name=getUsers)
			assert getUsers.password==generate_passwords("Password@123")
			assert len(getUsers.hashkey)==10
		assert Users.objects.count()==AccessManagement.objects.count()
		assert len(Users.objects.filter(active=False,user_verified=True))==3
		assert len(Users.objects.filter(active=True,user_verified=False))==3
		assert len(Users.objects.filter(active=False))==5
		assert len(Users.objects.filter(user_verified=False))==5
		assert len(Users.objects.filter(active=False,user_verified=False))==2
	
	@pytest.mark.parametrize("email,status,user_verified",[
	("testuser1@kpmg.com",True,False),("testuser2@kpmg.com",True,False),("testuser3@kpmg.com",True,False),
	("testuser4@kpmg.com",False,True),("testuser5@kpmg.com",False,True),("testuser6@kpmg.com",False,True),
	("testuser7@kpmg.com",False,False),("testuser8@kpmg.com",False,False)
		])	  
	def test_user_status(self,email,status,user_verified,setup_random_user):
		users=setup_random_user
		for obj in users:
			getUsers=Users.objects.create(**obj)
			getAccess=AccessManagement.objects.create(name=getUsers)
		getUsers=Users.objects.filter(email=email)
		getAccess=AccessManagement.objects.filter(name=getUsers[0])
		assert getUsers[0].email==email
		assert getUsers[0].active==status
		assert getUsers[0].user_verified==user_verified
		assert getUsers[0].password==generate_passwords("Password@123")
		assert getUsers[0].token==Users.objects.get(email=email).token
		assert getUsers[0].reporting_manager_id==None
		assert getUsers[0].reporting_manager_name==None
		assert getUsers[0].reporting_manager_email==None
		assert getAccess[0].name.email==email
		
	@pytest.mark.parametrize("email,status,user_verified",[
	("testuser1@kpmg.com",True,False),("testuser2@kpmg.com",True,False),("testuser3@kpmg.com",True,False),
	("testuser4@kpmg.com",False,True),("testuser5@kpmg.com",False,True),("testuser6@kpmg.com",False,True),
	("testuser7@kpmg.com",False,False),("testuser8@kpmg.com",False,False)
		])	
	def test_access_status(self,email,status,user_verified,setup_saved_user):
		getAccess=AccessManagement.objects.get(name__email=email)
		
		assert getAccess.name.active==status
		assert getAccess.name.user_verified==user_verified
		assert getAccess.name.password==generate_passwords("Password@123")
		assert getAccess.name.token==Users.objects.get(email=email).token
		assert getAccess.password_attempts ==0
		assert getAccess.last_login_attempt==None
		assert getAccess.otp ==None
		assert getAccess.otp_expiry_time ==None
		assert getAccess.last_otp_attempt==None
		assert getAccess.otp_attempts ==0
		assert getAccess.last_password_reset_request ==None
		assert getAccess.password_reset_request_count== 0
		assert getAccess.verification_link_expiry==None
		
	def test_all_access_status(self,setup_user):
	 
		users=setup_user
		for obj in users:
			getUsers=Users.objects.create(**obj)
			getAccess=AccessManagement.objects.create(name=getUsers)
		
		for user in Users.objects.all(): 
			getAccess=AccessManagement.objects.get(name__email=user.email)
			assert getAccess.name.active==True
			assert getAccess.name.user_verified==True
			assert getAccess.name.password==generate_passwords("Password@123")
			assert getAccess.name.token==user.token
			assert getAccess.password_attempts ==0
			assert getAccess.last_login_attempt==None
			assert getAccess.otp ==None
			assert getAccess.otp_expiry_time ==None
			assert getAccess.last_otp_attempt==None
			assert getAccess.otp_attempts ==0
			assert getAccess.last_password_reset_request ==None
			assert getAccess.password_reset_request_count== 0
			assert getAccess.verification_link_expiry==None
			
    
	
	
	
	  
		
		