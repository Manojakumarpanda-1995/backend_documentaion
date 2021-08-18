import ast
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
from datetime import datetime,timedelta


class Test_users_models():
	
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
		("testuser1@kpmg.com",True,False),("testuser2@kpmg.com",True,False)
		,("testuser3@kpmg.com",True,False),
		("testuser4@kpmg.com",False,True),("testuser5@kpmg.com",False,True)
		,("testuser6@kpmg.com",False,True),
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
		("testuser1@kpmg.com",True,False),("testuser2@kpmg.com",True,False)
		,("testuser3@kpmg.com",True,False),
		("testuser4@kpmg.com",False,True),("testuser5@kpmg.com",False,True)
		,("testuser6@kpmg.com",False,True),
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
			
	def test_roles(self):
		getRoles=Roles.objects.all()
		assert Roles.objects.count()==4
		getRoles=Roles.objects.create(role_name="Admins"
									,created_by=Users.objects.get(id=1)
									,updated_by=Users.objects.get(id=1))
		assert Roles.objects.count()==5
	
	@pytest.mark.parametrize("id,role_name",[(1,"SUPER-USER"),(4,"USER")
                                ,(3,"PROJECT-ADMIN"),(2,"COMPANY-ADMIN")
                                ,(5,"ADMINS")])
	def test_roles(self,id,role_name):
		assert Roles.objects.count()==4
		getRoles=Roles.objects.create(role_name="Admins"
									,created_by=Users.objects.get(id=1)
									,updated_by=Users.objects.get(id=1))
		assert Roles.objects.count()==5
		getRoles=Roles.objects.get(id=id)
		assert getRoles.role_name.upper()==role_name
		assert getRoles.created_by_id==Users.objects.get(id=1).id
		assert getRoles.updated_by_id==Users.objects.get(id=1).id

	@pytest.mark.parametrize("email,status,user_verified",[
		("testuser1@kpmg.com",True,False),("testuser2@kpmg.com",True,False)
		,("testuser3@kpmg.com",True,False),
		("testuser4@kpmg.com",False,True),("testuser5@kpmg.com",False,True)
		,("testuser6@kpmg.com",False,True),
		("testuser7@kpmg.com",False,False),("testuser8@kpmg.com",False,False)
		])
	def test_temporaryurl(self,email,status,user_verified,setup_temporary_urls):
		
		users=setup_temporary_urls
		assert TemporaryURL.objects.count()==len(users)
		getUrl=TemporaryURL.objects.filter(user__email=email)
		assert getUrl[0].expiry_time is not None
		# assert getUrl[0].expiry_time==datetime.now()
		assert len(getUrl[0].filename.split("."))==2
		assert len(getUrl[0].filepath.split("/"))==4
		assert "xlsx" in getUrl[0].filename.split(".")
		assert "" in getUrl[0].filepath.split("/")
		assert getUrl[0].token==Users.objects.get(email=email).token
		assert getUrl[0].user.token==Users.objects.get(email=email).token
		assert getUrl[0].user.active==status
		assert getUrl[0].user.user_verified==user_verified
   
	def test_temporary_url(self,setup_temporary_urls):
		
		users=setup_temporary_urls
		assert TemporaryURL.objects.count()==len(users)
		for x in range(len(users)):
			getUrl=TemporaryURL.objects.filter(user__email=users[x]["email"])
			assert getUrl[0].expiry_time is not None
			# assert getUrl[0].expiry_time==datetime.now()
			assert len(getUrl[0].filename.split("."))==2
			assert len(getUrl[0].filepath.split("/"))==4
			assert "xlsx" in getUrl[0].filename.split(".")
			assert "" in getUrl[0].filepath.split("/")
			assert getUrl[0].token==Users.objects.get(email=users[x]["email"]).token
			assert getUrl[0].user.token==Users.objects.get(email=users[x]["email"]).token
   
	@pytest.mark.parametrize("email,status,user_verified",[
		("testuser1@kpmg.com",True,False),("testuser2@kpmg.com",True,False)
		,("testuser3@kpmg.com",True,False),
		("testuser4@kpmg.com",False,True),("testuser5@kpmg.com",False,True)
		,("testuser6@kpmg.com",False,True),
		("testuser7@kpmg.com",False,False),("testuser8@kpmg.com",False,False)
		])
	def test_activitylogs(self,email,status,user_verified,setup_activitylogs):
		
		users=setup_activitylogs
		assert ActivityLogs.objects.count()==len(users)
		getActivity=ActivityLogs.objects.filter(user__email=email)
		assert getActivity[0].timestamp is not None
		assert len(getActivity[0].activity)<=70
		assert len(getActivity[0].ip_address.split("."))==4
		assert getActivity[0].user.token==Users.objects.get(email=email).token
		assert getActivity[0].user.active==status
		assert getActivity[0].user.user_verified==user_verified
   
	def test_activity_logs(self,setup_activitylogs):
		users=setup_activitylogs
		for x in range(len(users)):
			assert ActivityLogs.objects.count()==len(users)
			getActivity=ActivityLogs.objects.filter(user__email=users[x]["email"])
			assert getActivity[0].timestamp is not None
			assert len(getActivity[0].activity)<=70
			assert len(getActivity[0].ip_address.split("."))==4
			assert getActivity[0].user.token==Users.objects.get(email=users[x]["email"]).token
		

class Test_worker_models():
    
	def test_worker(self,setup_register_worker):
		getWorker=Workers.objects.get(id=1)
		assert getWorker.name=="Rohit"		
		assert getWorker.email.endswith('@momenttext.com')		
		assert getWorker.email.startswith('Rohit')	
		assert getWorker.active==True	
		assert len(getWorker.phone_no)==10
		assert ast.literal_eval(getWorker.skill_sets)==["java","c++","jquery"]
		assert "python" not in getWorker.skill_sets
		assert Workers.objects.count()==6
  
	def test_worker_all(self,setup_register_worker):
		companies=setup_register_worker
		for company in companies:
			getWorker=Workers.objects.get(name=company['name'])
			assert getWorker.name==company["name"]	
			assert getWorker.email.endswith('@momenttext.com')	
			assert getWorker.active==True	
			assert len(getWorker.phone_no)==10
			assert ast.literal_eval(getWorker.skill_sets)==["java","c++","jquery"]
			assert "python" not in getWorker.skill_sets
			assert Workers.objects.count()==6
  
class Test_access_request_models():
    
	def test_worker(self,setup_register_access):
		getAccessRequest=AccessRequest.objects.get(id=1)
		assert getAccessRequest.name=="Nitin"		
		assert getAccessRequest.company_name=="Amazon"		
		assert getAccessRequest.email.endswith('@momenttext.com')		
		assert getAccessRequest.email.startswith('Nitin')	
		assert getAccessRequest.active==True	
		assert len(getAccessRequest.phone_number)==10
		assert ast.literal_eval(getAccessRequest.skill_sets)==["java","c++","jquery"]
		assert "python" not in getAccessRequest.skill_sets
		assert AccessRequest.objects.count()==6
  
	def test_worker_all(self,setup_register_access):
		companies=setup_register_access
		for company in companies:
			getAccessRequest=AccessRequest.objects.get(name=company['name'])
			assert getAccessRequest.name==company["name"]	
			assert getAccessRequest.company_name==company["company_name"]	
			assert getAccessRequest.email.endswith('@momenttext.com')	
			assert getAccessRequest.active==False	
			assert len(getAccessRequest.phone_number)==10
			assert ast.literal_eval(getAccessRequest.skill_sets)==["java","c++","jquery"]
			assert "python" not in getAccessRequest.skill_sets
			assert AccessRequest.objects.count()==6
			assert len(AccessRequest.objects.filter(active=False))==5
			assert len(AccessRequest.objects.filter(active=False,pending_status=True))==5
			assert len(AccessRequest.objects.filter(active=False,pending_status=False))==0
  
  
  
  
	
	
	
	  
		
		