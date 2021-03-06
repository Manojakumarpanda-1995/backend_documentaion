import random
import string
import pytest
import faker
import hashlib
# from usermanagement.utils.store_activity_logs import func_store_activity_logs
from django.conf import settings
from django.utils import timezone
from organization.models import *
from project.models import *
from project.models import ActivityLogs as ActivityLog
from usermanagement.models import *
from usermanagement.models import AccessManagement, Users
from usermanagement.utils.hash import (decryption, encryption,removeSpecialCharacters
									   ,generate_passwords)

refresh_lockout = getattr(settings, "LOCKOUT_COUNT_RESET_DURATION", None)
time_threshold = getattr(settings, "INCORRECT_PASSWORD_COUNT_THRESHOLD", None)
count_threshold = getattr(settings, "INCORRECT_PASSWORD_COUNT_MAX_ATTEMPTS", None)
superuser = getattr(settings, "SUPERUSER", None)
superuser_pass = getattr(settings, "SUPERUSERPASS", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)
secret = getattr(settings, "SECRET_KEY", None)
import logging
import os
import sys
import uuid
from datetime import datetime, timedelta
fake=faker.Faker()

pytestmark=pytest.mark.django_db
@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
	pass


##Setup for the usermanagement
@pytest.fixture(autouse=True)
def setup_superusers():

	users = [{
		"first_name": "Super",
		"last_name": " User 1",
		"name": "backend Super User 1",
		"email": "su1@momenttext.com",
		"password": generate_passwords("Password@123"),
		"token": uuid.uuid4().hex,
		"designation": "Test",
		"active": True,
		"user_verified": True,
		"reporting_manager_id": "67890",
		"reporting_manager_name": "Rohit Khandelwal",
		"reporting_manager_email": "Rohitkhandelwal@momenttext.com",
		"hashkey": uuid.uuid1().hex
	}]
	for user in users:
		isAlreadyAvailable = Users.objects.filter(email=user["email"])
		if len(isAlreadyAvailable) == 0:
			user = Users.objects.create(**user)
			AccessManagement.objects.create(name=user)
		else:
			isAccesManageAvailable = AccessManagement.objects.filter(name=isAlreadyAvailable[0])
			if len(isAccesManageAvailable) == 0:
				AccessManagement.objects.create(name=isAlreadyAvailable[0])

@pytest.fixture(autouse=True)
def setup_roles(setup_superusers):
	roles = [
		{"role_name": "SUPER-USER","created_by": 1,"updated_by": 1},
		{"role_name": "COMPANY-ADMIN","created_by": 1,"updated_by": 1},
		{"role_name": "PROJECT-ADMIN","created_by": 1,"updated_by": 1},
		{"role_name": "USER","created_by": 1,"updated_by": 1}]

	for role in roles:
		getRole = Roles.objects.filter(role_name=role["role_name"].upper())
		if len(getRole) == 0:
			role["created_by"] = Users.objects.filter(id=role["created_by"])[0]
			role["updated_by"] = Users.objects.filter(id=role["updated_by"])[0]
			getRole = Roles.objects.create(**role)

@pytest.fixture(autouse=True)
def setup_company(setup_superusers):
	try:
		getSuperUser= Users.objects.filter(id=1)[0]
		companies =[{"name": "Administrator","created_by":getSuperUser,"updated_by":getSuperUser}
				,{"name": "Google","created_by":getSuperUser,"updated_by": getSuperUser}
				,{"name":"Gmail","created_by":getSuperUser,"updated_by":getSuperUser}
				,{"name":"Amazon","created_by":getSuperUser,"updated_by":getSuperUser}
				,{"name":"Tesla","created_by":getSuperUser,"updated_by":getSuperUser}
				,{"name":"Infosys","created_by":getSuperUser,"updated_by":getSuperUser}
				,{"name":"Tata","created_by":getSuperUser,"updated_by":getSuperUser}
				]	
		for company in companies:
			getCompany = Company.objects.create(**company)

			getCompanyInfo,created=CompanyInfo.objects.get_or_create(company=getCompany
										,created_by=Users.objects.get(id=1)
										,updated_by=Users.objects.get(id=1))
			getCompanyInfo.logo = fake.image_url()
			getCompanyInfo.corporate_type ="Health Insurance"
			getCompanyInfo.number_of_emploies=fake.building_number()
			getCompanyInfo.type="Health"
			getCompanyInfo.links =fake.url()
			getCompanyInfo.about=fake.text(max_nb_chars=500)
			getCompanyInfo.active=True
			getCompanyInfo.save()

			#Creating project for all company
			getUser=Users.objects.get(email="su1@momenttext.com")
			name="{} project1".format(getCompany.name)
			project_name_hash = hashlib.sha256(" ".join([removeSpecialCharacters(getCompany.name +name)
                                                , secret]).encode()).hexdigest()
			getProjectInfo=ProjectInfo.objects.create(project_name_hash =project_name_hash
				,project_id =fake.uuid4(),name=name
				,description =fake.text()
				,catagory =fake.name()
				,salary_from=int(''.join(random.choice(string.digits) for x in range(4)))
				,salary_to=int(''.join(random.choice(string.digits) for x in range(4)))
				,start_date=fake.date(),end_date=fake.date()
				,start_time=fake.time(),end_time=fake.time(),created_by =getUser,updated_by=getUser)
   
	except Exception as e:
		print("Exception at==>",e)

@pytest.fixture(autouse=True)
def setup_company_role(setup_superusers,setup_roles):
	companyRole={"user": 1,"company": 1,"role": 1,"created_by": 1,"updated_by": 1,}
	companyRole["created_by"] = Users.objects.filter(id=companyRole["created_by"])[0]
	companyRole["updated_by"] = Users.objects.filter(id=companyRole["updated_by"])[0]
	companyRole["user"] = Users.objects.filter(id=companyRole["user"])[0]
	companyRole["company"] = Company.objects.filter(id=companyRole["company"])[0]
	companyRole["role"] = Roles.objects.filter(id=companyRole["role"])[0]
	getUserCompanyRole = UserCompanyRole.objects.create(**companyRole)
 
@pytest.fixture
def setup_user():
	user=[
		{"first_name":"Test","last_name":"User1"
			,"name":"Test User1","email":"test_user1@momenttext.com"
			,"password":generate_passwords("Password@123"),"hashkey":uuid.uuid4().hex[:10]		
			,"token":uuid.uuid4().hex,"designation":"Employee"
			,"active":True,"user_verified":True
			,"reporting_manager_id":"67890","reporting_manager_name":"Rohit Khandelwal"
			,"reporting_manager_email":"Rohitkhandelwal@momenttext.com"}
		,{"first_name":"Test","last_name":"User3"
			,"name":"Test User3","email":"test_user3@momenttext.com"
			,"password":generate_passwords("Password@123"),"hashkey":uuid.uuid4().hex[:10]		
			,"token":uuid.uuid4().hex,"designation":"Employee"
			,"active":True,"user_verified":True
			,"reporting_manager_id":"67890","reporting_manager_name":"Rohit Khandelwal"
			,"reporting_manager_email":"Rohitkhandelwal@momenttext.com"}
		,{"first_name":"Test","last_name":"User2"
			,"name":"Test User2","email":"test_user2@momenttext.com"
			,"password":generate_passwords("Password@123"),"hashkey":uuid.uuid4().hex[:10]		
			,"token":uuid.uuid4().hex,"designation":"Employee"
			,"active":True,"user_verified":True
			,"reporting_manager_id":"67890","reporting_manager_name":"Rohit Khandelwal"
			,"reporting_manager_email":"Rohitkhandelwal@momenttext.com"}
	]
	
	return user

@pytest.fixture
def setup_random_user():
	users=[
		{"first_name":"test","last_name":"user1","email":"testuser1@momenttext.com","active":True
		,"user_verified":False,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		},
		{"first_name":"test","last_name":"user2","email":"testuser2@momenttext.com","active":True
		,"user_verified":False,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		},
		{"first_name":"test","last_name":"user3","email":"testuser3@momenttext.com","active":True
		,"user_verified":False,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		},
		{"first_name":"test","last_name":"user4","email":"testuser4@momenttext.com","active":False
		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		}
		,{"first_name":"test","last_name":"user5","email":"testuser5@momenttext.com","active":False
		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		}
		,{"first_name":"test","last_name":"user6","email":"testuser6@momenttext.com","active":False
		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		}
		,{"first_name":"test","last_name":"user1","email":"testuser7@momenttext.com","active":False
		,"user_verified":False,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		}
		,{"first_name":"test","last_name":"user1","email":"testuser8@momenttext.com","active":False
		,"user_verified":False,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		}
	]
	return users

@pytest.fixture
def setup_user_without_access():
	users=[
		{"first_name":"test","last_name":"user1","email":"testuser1@momenttext.com","active":True
		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		},
		{"first_name":"test","last_name":"user2","email":"testuser2@momenttext.com","active":True
		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		},
		{"first_name":"test","last_name":"user3","email":"testuser3@momenttext.com","active":True
		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		},
		{"first_name":"test","last_name":"user4","email":"testuser4@momenttext.com","active":True
		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		}
		
	]
	
	for obj in users:
		getUsers=Users.objects.create(**obj)
	return users

@pytest.fixture
def setup_saved_user():
	users=[
		{"first_name":"test","last_name":"user1","email":"testuser1@momenttext.com","active":True
		,"user_verified":False,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		},
		{"first_name":"test","last_name":"user2","email":"testuser2@momenttext.com","active":True
		,"user_verified":False,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		},
		{"first_name":"test","last_name":"user3","email":"testuser3@momenttext.com","active":True
		,"user_verified":False,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		},
		{"first_name":"test","last_name":"user4","email":"testuser4@momenttext.com","active":False
		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		}
		,{"first_name":"test","last_name":"user5","email":"testuser5@momenttext.com","active":False
		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		}
		,{"first_name":"test","last_name":"user6","email":"testuser6@momenttext.com","active":False
		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		}
		,{"first_name":"test","last_name":"user1","email":"testuser7@momenttext.com","active":False
		,"user_verified":False,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		}
		,{"first_name":"test","last_name":"user1","email":"testuser8@momenttext.com","active":False
		,"user_verified":False,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		}
	]
	otp=""
	for obj in users:
		getUsers=Users.objects.create(**obj)
		getAccess=AccessManagement.objects.create(name=getUsers)
	return users
		
@pytest.fixture  
def setup_update_password(setup_random_user):
	users=setup_random_user  
	for x in range(len(users)//2):
		getUsers=Users.objects.create(**users[x])
		getAccess=AccessManagement.objects.create(name=getUsers)
		getAccess.otp=encryption("4yT28GN7")
		getAccess.otp_expiry_time=datetime.now(tz=timezone.utc)+timedelta(minutes=20)
		getAccess.otp_attempts = 2
		getAccess.save()
  
	for x in range(len(users)//2,len(users)):
		getUsers=Users.objects.create(**users[x])
		getAccess=AccessManagement.objects.create(name=getUsers)
		getAccess.otp=encryption("4yT28GN7")
		getAccess.otp_attempts=2
		getAccess.otp_expiry_time=datetime.now(tz=timezone.utc)-timedelta(minutes=20)
		getAccess.save()

@pytest.fixture
def setup_temporary_urls(setup_saved_user,setup_random_user):
	users=setup_random_user
	
	for x in range(len(users)):
		getUser=Users.objects.get(email__iexact=users[x]["email"])
		temporary_url={"user":getUser
				,"token":getUser.token
				,"filename":fake.file_name(category="file",extension="xlsx")
				,"filepath":fake.file_path(depth=2,category="file",extension="xlsx")
				,"expiry_time":datetime.now(tz=timezone.utc)
				}

		getTemporaryurl=TemporaryURL.objects.create(**temporary_url)
	
	return users 

@pytest.fixture
def setup_activitylogs(setup_saved_user):
	users=setup_saved_user
	
	for x in range(len(users)):
		getUser=Users.objects.get(email__iexact=users[x]["email"])
		activity_logs={"user":getUser
				,"activity":fake.text(max_nb_chars=70)
				,"ip_address":fake.ipv4()
				,"timestamp":datetime.now(tz=timezone.utc)
				}

		getActivityLogs=ActivityLogs.objects.create(**activity_logs)
	
	return users 

@pytest.fixture
def setup_register_worker(setup_saved_user):
	worker_data=[]
	worker={"name":"Rohit","email":"Rohit@momenttext.com","active":True
			,"phone_no":"".join((random.choice(string.digits) for i in range(10)))
			,"skill_sets":["java","c++","jquery"]
			,"created_at":fake.date_time(tzinfo=timezone.utc)
			,"updated_at":fake.date_time(tzinfo=timezone.utc)}
	getWorker=Workers.objects.create(**worker)

	for obj in range(5):
		worker={"name":fake.name(),"email":fake.email(domain="momenttext.com"),"active":True
				,"phone_no":"".join((random.choice(string.digits) for i in range(10)))
				,"skill_sets":["java","c++","jquery"]
				,"created_at":fake.date_time(tzinfo=timezone.utc)
				,"updated_at":fake.date_time(tzinfo=timezone.utc)}
		worker_data.append(worker)
		getWorker=Workers.objects.create(**worker)

	return worker_data

@pytest.fixture
def setup_register_access(setup_saved_user):
	access_data=[]
	access={"company_name":"Amazon","name":"Nitin","email":"Nitin@momenttext.com"
			,"phone_number":"".join((random.choice(string.digits) for i in range(10)))
			,"skill_sets":["java","c++","jquery"]
			,"created_at":fake.date_time(tzinfo=timezone.utc)
			,"updated_at":fake.date_time(tzinfo=timezone.utc)}
	getWorker=AccessRequest.objects.create(**access)

	for obj in range(5):
		access={"name":fake.name(),"company_name":fake.company()
				,"email":fake.email(domain="momenttext.com"),"active":False
				,"phone_number":"".join((random.choice(string.digits) for i in range(10)))
				,"skill_sets":["java","c++","jquery"]
				,"created_at":fake.date_time(tzinfo=timezone.utc)
				,"updated_at":fake.date_time(tzinfo=timezone.utc)}
		access_data.append(access)
		getWorker=AccessRequest.objects.create(**access)

	return access_data

@pytest.fixture
def setup_multiple_invalid(setup_saved_user):
	
	users=Users.objects.exclude(id=1)
	for user in users:
		getAccess=AccessManagement.objects.get(name=user)
		getAccess.last_login_attempt=(datetime.now(tz=timezone.utc)
                                +timedelta(minutes=refresh_lockout+5))
		getAccess.password_attempts=count_threshold
		getAccess.save()
	
@pytest.fixture
def setup_multiple_invalid_reset(setup_saved_user):
	
	users=Users.objects.exclude(id=1)
	for user in users:
		getAccess=AccessManagement.objects.get(name=user)
		getAccess.last_login_attempt=(datetime.now(tz=timezone.utc)
                                -timedelta(minutes=refresh_lockout+5))
		getAccess.password_attempts=count_threshold
		getAccess.save()
	
@pytest.fixture
def setup_invalid_attempt_update(setup_saved_user):
	
	users=Users.objects.exclude(id=1)
	for user in users:
		getAccess=AccessManagement.objects.get(name=user)
		getAccess.last_login_attempt=(datetime.now(tz=timezone.utc)
                                -timedelta(minutes=refresh_lockout+5))
		getAccess.password_attempts=count_threshold-3
		getAccess.save()
	
@pytest.fixture
def setup_invalid_first_attempt(setup_saved_user):
	
	users=Users.objects.exclude(id=1)
	for user in users:
		getAccess=AccessManagement.objects.get(name=user)
		getAccess.last_login_attempt=(datetime.now(tz=timezone.utc)
                                -timedelta(minutes=refresh_lockout-5))
		getAccess.password_attempts=6
		getAccess.save()

@pytest.fixture
def setup_multiple_invalid_for_pass_reset(setup_saved_user):
	
	users=Users.objects.exclude(email__in=["su1@momenttext.com","companyadmin@momenttext.com"
                                        ,"testuser@momenttext.com","user@momenttext.com"
                                        ,"projectadmin@momenttext.com"])
	for x in range(len(users)//2):
		getAccess=AccessManagement.objects.get(name=users[x])
		getAccess.last_password_reset_request=(datetime.now(tz=timezone.utc)
                                +timedelta(minutes=refresh_lockout+5))
		getAccess.password_reset_request_count=count_threshold
		getAccess.save()
	for x in range(len(users)//2,len(users)):
		getAccess=AccessManagement.objects.get(name=users[x])
		getAccess.last_password_reset_request=(datetime.now(tz=timezone.utc)
                                -timedelta(minutes=refresh_lockout+5))
		getAccess.password_reset_request_count=count_threshold
		getAccess.save()
	
@pytest.fixture
def setup_update_password_access_counter(setup_saved_user):
	
	users=Users.objects.exclude(email__in=["su1@momenttext.com","companyadmin@momenttext.com"
                                        ,"testuser@momenttext.com","user@momenttext.com"
                                        ,"projectadmin@momenttext.com"])
	for x in range(len(users)//2):
		getAccess=AccessManagement.objects.get(name=users[x])
		getAccess.last_password_reset_request=(datetime.now(tz=timezone.utc)
                                +timedelta(minutes=refresh_lockout+5))
		getAccess.last_otp_attempt=(datetime.now(tz=timezone.utc)
                                +timedelta(minutes=refresh_lockout+5))
		getAccess.otp_expiry_time=(datetime.now(tz=timezone.utc)
                                +timedelta(minutes=refresh_lockout+5))
		getAccess.password_reset_request_count=2
		getAccess.otp_attempts=4
		getAccess.otp=encryption("yGTN8427")
		getAccess.save()
	for x in range(len(users)//2,len(users)):
		getAccess=AccessManagement.objects.get(name=users[x])
		getAccess.last_password_reset_request=(datetime.now(tz=timezone.utc)
                                -timedelta(minutes=refresh_lockout+5))
		getAccess.last_otp_attempt=(datetime.now(tz=timezone.utc)
                                -timedelta(minutes=refresh_lockout+5))
		getAccess.otp_expiry_time=(datetime.now(tz=timezone.utc)
                                +timedelta(minutes=refresh_lockout+5))
		getAccess.password_reset_request_count=3
		getAccess.otp_attempts=4
		getAccess.otp=encryption("yGTN8427")
		getAccess.save()
	
@pytest.fixture
def setup_user_for_new_password():
	users=[
		{"first_name":"test","last_name":"user1","email":"testuser1@momenttext.com","active":True
		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		},
		{"first_name":"test","last_name":"user2","email":"testuser2@momenttext.com","active":True
		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		},
		{"first_name":"test","last_name":"user3","email":"testuser3@momenttext.com","active":True
		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		},
		{"first_name":"test","last_name":"user4","email":"testuser4@momenttext.com","active":True
		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		}
		,{"first_name":"test","last_name":"user5","email":"testuser5@momenttext.com","active":True
		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		}
		,{"first_name":"test","last_name":"user6","email":"testuser6@momenttext.com","active":True
		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		}
		,{"first_name":"test","last_name":"user7","email":"testuser7@momenttext.com","active":True
		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		}
		,{"first_name":"test","last_name":"user8","email":"testuser8@momenttext.com","active":True
		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
		}
	]
	otp=""
	for obj in users:
		getUsers=Users.objects.create(**obj)
		getAccess=AccessManagement.objects.create(name=getUsers)
	return users

@pytest.fixture(autouse=True)
def setup_users_roles(setup_superusers,setup_roles):
	try:
		users=[
			{"first_name":"Company","last_name":"Admin","email":"companyadmin@momenttext.com","active":True
			,"user_verified":True,"password":generate_passwords("Password@1234567"),"token":fake.uuid4()
			,"hashkey":fake.uuid4()[:10],
			},
			{"first_name":"Project","last_name":"Admin","email":"projectadmin@momenttext.com","active":True
			,"user_verified":True,"password":generate_passwords("Password@1237654"),"token":fake.uuid4()
			,"hashkey":fake.uuid4()[:10],
			},
			{"first_name":"Test","last_name":"User","email":"testuser@momenttext.com","active":True
			,"user_verified":True,"password":generate_passwords("Password@1232424"),"token":fake.uuid4()
			,"hashkey":fake.uuid4()[:10],
			},
			{"first_name":"End","last_name":"User","email":"user@momenttext.com","active":True
			,"user_verified":True,"password":generate_passwords("Password@1231212"),"token":fake.uuid4()
			,"hashkey":fake.uuid4()[:10],
			}
			]
	
		getSuperUser= Users.objects.filter(id=1)[0]
		company ={"name": "Microsoft","created_by":getSuperUser,"updated_by": getSuperUser}
		getCompany = Company.objects.create(**company)
		#Creating project for all company
		getUser=Users.objects.get(email="su1@momenttext.com")
		name="{} project1".format(getCompany.name)
		project_name_hash = hashlib.sha256(" ".join([removeSpecialCharacters(getCompany.name +name)
                                            , secret]).encode()).hexdigest()
		getProjectInfo=ProjectInfo.objects.create(project_name_hash =project_name_hash
			,project_id =fake.uuid4(),name=name
			,description =fake.text()
			,catagory =fake.name()
			,salary_from=int(''.join(random.choice(string.digits) for x in range(4)))
			,salary_to=int(''.join(random.choice(string.digits) for x in range(4)))
			,start_time=fake.time(),end_time=fake.time(),created_by =getUser,updated_by=getUser)
		getCompanyInfo=CompanyInfo.objects.get_or_create(company=getCompany)
		roles=[2,3,4,4]
		for x in range(len(users)):
			users[x]["name"]=users[x]["first_name"]+" "+users[x]["last_name"]
			getUser=Users.objects.create(**users[x])
			getAccess=AccessManagement.objects.create(name=getUser)
			companyRole={"role":roles[x]}
			companyRole["created_by"] =getSuperUser
			companyRole["updated_by"] =getSuperUser
			companyRole["user"] =getUser
			companyRole["company"] = getCompany
			companyRole["role"] = Roles.objects.filter(id=roles[x])[0]
			getUserCompanyRole = UserCompanyRole.objects.create(**companyRole)
			if roles[x]==3:
				getProjectUser=ProjectUsers.objects.create(user=getUserCompanyRole,project=getProjectInfo
                                               ,created_by=getSuperUser,updated_by=getSuperUser)
		return users
	except Exception as e:
		print("Exception at==>",e)


##Setup for organizations
@pytest.fixture
def setup_test_company(setup_superusers):
	try:
		getSuperUser= Users.objects.filter(id=1)[0]
		companies =[{"name": "Momenttext","address1":fake.address(),"active":False,"city":fake.city()
				,"state":fake.state(),"country":fake.country(),"state_pin_code":fake.postcode()
				,"partner_name":fake.name(),"state_pin_code":fake.postalcode()}
				,{"name":"Allen Solly","address1":fake.address(),"active":True,"city":fake.city()
				,"state":fake.state(),"country":fake.country(),"state_pin_code":fake.postcode()
				,"partner_name":fake.name(),"state_pin_code":fake.postalcode()}
				,{"name":"Honda","address1":fake.address(),"active":False,"city":fake.city()
				,"state":fake.state(),"country":fake.country(),"state_pin_code":fake.postcode()
				,"partner_name":fake.name(),"state_pin_code":fake.postalcode()}
				,{"name":"Mahindra","address1":fake.address(),"active":True,"city":fake.city()
				,"state":fake.state(),"country":fake.country(),"state_pin_code":fake.postcode()
				,"partner_name":fake.name(),"state_pin_code":fake.postalcode()}
				,{"name":"Peter England","address1":fake.address(),"active":False,"city":fake.city()
				,"state":fake.state(),"country":fake.country(),"state_pin_code":fake.postcode()
				,"partner_name":fake.name(),"state_pin_code":fake.postalcode()}
				]	
		for company in companies:
			company["created_by"]=getSuperUser
			company["updated_by"]=getSuperUser
			getCompany = Company.objects.create(**company)
		return companies
	except Exception as e:
		print("Exception at==>",e)
 
@pytest.fixture
def setup_company_info(setup_test_company):
	getCompanies=setup_test_company
	companyinfo=[]
	for company in getCompanies:
		getCompany=Company.objects.get(name=company["name"])
		getCompanyInfo,created=CompanyInfo.objects.get_or_create(company=getCompany
										,created_by=Users.objects.get(id=1)
										,updated_by=Users.objects.get(id=1))
		getCompanyInfo.logo = fake.image_url()
		getCompanyInfo.corporate_type ="Health Insurance"
		getCompanyInfo.number_of_emploies=fake.building_number()
		getCompanyInfo.type="Health"
		getCompanyInfo.links =fake.url()
		getCompanyInfo.about=fake.text(max_nb_chars=500)
		status=fake.boolean()
		getCompanyInfo.active=status
		getCompanyInfo.save()
		companyinfo.append({"company":company["name"],"status":status})

	return companyinfo

@pytest.fixture    
def setup_usercompany_role(setup_random_user):
	try:
		users=setup_random_user

		#To list all user
		companies=[fake.company() for x in range(4)]
		for company in companies:
			getCompany=Company.objects.create(name=company,created_by=Users.objects.get(id=1)
												,updated_by=Users.objects.get(id=1))
		
		#To list all company
		company1=Company.objects.get(name=companies[0])
		company2=Company.objects.get(name=companies[1])
		company3=Company.objects.get(name=companies[2])
		company4=Company.objects.get(name=companies[3])
	
		for user in users:
			getUsers=Users.objects.create(**user)

		#To list all users
		user1=Users.objects.get(email="testuser1@momenttext.com")
		user2=Users.objects.get(email="testuser2@momenttext.com")
		user3=Users.objects.get(email="testuser3@momenttext.com")
		user4=Users.objects.get(email="testuser4@momenttext.com")
		user5=Users.objects.get(email="testuser5@momenttext.com")
		user6=Users.objects.get(email="testuser6@momenttext.com")
		company_admin=Roles.objects.get(id=2)
		project_admin=Roles.objects.get(id=3)
		user=Roles.objects.get(id=4)
		#Users 1 with company 1,2,3 all user
		getUserCompanyRoles=[{"user":user1,"company":company2,"role":company_admin}
							,{"user":user1,"company":company3,"role":company_admin}
							,{"user":user2,"company":company2,"role":project_admin}
							,{"user":user2,"company":company3,"role":project_admin}
							,{"user":user3,"company":company1,"role":project_admin}
							,{"user":user3,"company":company3,"role":user}
							,{"user":user4,"company":company4,"role":company_admin}
							,{"user":user5,"company":company4,"role":user}
							,{"user":user6,"company":company1,"role":user}
							,{"user":user6,"company":company2,"role":user}
							,{"user":user6,"company":company3,"role":user}
							,{"user":user6,"company":company4,"role":user}
							]
		for obj in getUserCompanyRoles:
			obj["created_by"]=Users.objects.get(id=1)
			obj["updated_by"]=Users.objects.get(id=1)
			getUserCompanyRole=UserCompanyRole.objects.create(**obj)

		return companies
	except Exception as e:
		print("Exception at==>",e)

@pytest.fixture
def setup_list_company():
	
	getCompanies=Company.objects.exclude(name__in=["Administrator","Microsoft"])
	getRole=Roles.objects.get(id=2)
	getUsers=Users.objects.get(email="companyadmin@momenttext.com")
	for company in getCompanies:
		getUserCompanyRole=UserCompanyRole.objects.create(company=company
                                ,created_by_id=1
                                ,updated_by_id=1
								,role=getRole
								,user=getUsers)

@pytest.fixture    
def setup_list_company_byemail(setup_user_for_new_password):
	try:

		#To list all user
		companies=[fake.company() for x in range(4)]
		for company in companies:
			getCompany=Company.objects.create(name=company,created_by=Users.objects.get(id=1)
												,updated_by=Users.objects.get(id=1))
		
		#To list all company
		company1=Company.objects.get(name=companies[0])
		company2=Company.objects.get(name=companies[1])
		company3=Company.objects.get(name=companies[2])
		company4=Company.objects.get(name=companies[3])

		#To list all users
		user1=Users.objects.get(email="testuser1@momenttext.com")
		user2=Users.objects.get(email="testuser2@momenttext.com")
		user3=Users.objects.get(email="testuser3@momenttext.com")
		user4=Users.objects.get(email="testuser4@momenttext.com")
		user5=Users.objects.get(email="testuser5@momenttext.com")
		user6=Users.objects.get(email="testuser6@momenttext.com")
		company_admin=Roles.objects.get(id=2)
		project_admin=Roles.objects.get(id=3)
		user=Roles.objects.get(id=4)
		#Users 1 with company 1,2,3 all user
		getUserCompanyRoles=[{"user":user1,"company":company2,"role":company_admin}
							,{"user":user1,"company":company3,"role":company_admin}
							,{"user":user2,"company":company2,"role":project_admin}
							,{"user":user2,"company":company3,"role":project_admin}
							,{"user":user3,"company":company1,"role":project_admin}
							,{"user":user3,"company":company3,"role":user}
							,{"user":user4,"company":company4,"role":company_admin}
							,{"user":user5,"company":company4,"role":user}
							,{"user":user6,"company":company1,"role":user}
							,{"user":user6,"company":company2,"role":user}
							,{"user":user6,"company":company3,"role":user}
							,{"user":user6,"company":company4,"role":user}
							]
		for obj in getUserCompanyRoles:
			obj["created_by"]=Users.objects.get(id=1)
			obj["updated_by"]=Users.objects.get(id=1)
			getUserCompanyRole=UserCompanyRole.objects.create(**obj)

		return companies
	except Exception as e:
		print("Exception at==>",e)

@pytest.fixture
def setup_create_usercompanyrole_with_existing_companyrole(setup_user_for_new_password):
	users=["testuser{}@momenttext.com".format(x) for x in range(1,6)]
	getCompany=Company.objects.get(id=5)
	getRole=Roles.objects.get(id=3)
	getUser=Users.objects.get(email="su1@momenttext.com")
	for getUser in Users.objects.filter(email__in=users):
		getUserCompanyRole = UserCompanyRole.objects.create(user=getUser
                                ,isActive=False
                                ,created_by=getUser
                                ,updated_by=getUser
								, company=getCompany
								, role=getRole)

##Project management
@pytest.fixture
def setup_project_info(setup_superusers):
	try:
		getProject=[]
		for company in Company.objects.all():
      
			#Creating project for all company
			getUser=Users.objects.get(email="su1@momenttext.com")
			name=fake.company()
			project_name_hash = hashlib.sha256(" ".join([removeSpecialCharacters(company.name +name)
                                                , secret]).encode()).hexdigest()
			getProjectInfo=ProjectInfo.objects.create(project_name_hash =project_name_hash
				,project_id =fake.uuid4(),name=name
				,description =fake.text(),catagory =fake.name()
				,salary_from=int(''.join(random.choice(string.digits) for x in range(4)))
				,salary_to=int(''.join(random.choice(string.digits) for x in range(4)))
				,start_date=fake.date(),end_date=fake.date()
				,start_time=fake.time(),end_time=fake.time(),created_by =getUser,updated_by=getUser)
			getProject.append(name)
		return getProject
	except Exception as e:
		print("Exception at==>",e)
  
@pytest.fixture
def setup_projectusers(setup_user_for_new_password):
	try:
		getProject=[]
		getSuperUser=Users.objects.get(email="su1@momenttext.com")
		getCompany=Company.objects.all()
		for project in ProjectInfo.objects.all():
      
			for x in range(1,len(getCompany)+1):
				getUser=Users.objects.get(email="testuser{}@momenttext.com".format(x))
				getUserCompanyRole=UserCompanyRole.objects.create(role_id=3
                                                      ,user=getUser,created_by=getSuperUser
                                                      ,company_id=x,updated_by=getSuperUser)
				getProjectUsers=ProjectUsers.objects.create(project=project,user=getUserCompanyRole
                                                ,created_by=getSuperUser,updated_by=getSuperUser)
				
		return getProject
	except Exception as e:
		print("Exception at==>",e)

@pytest.fixture
def setup_fileupload():
    
	file_names=[]
	for obj in range(5):
		file_name={"original_file_name" :fake.file_name(category="file",extension='.xlsx')
			,"datafile":fake.file_path(depth=2,category="file",extension='xlsx')
			,"function_type" :fake.text(max_nb_chars=10),"created_by_id":1}
		getFileUpload=FileUpload.objects.create(**file_name)
		file_names.append(file_name)
	return file_names

@pytest.fixture
def setup_project_activitylog(setup_projectusers):
    
	activity_logs=[]
	for projectuser in ProjectUsers.objects.all():
		activity={"project_user":projectuser,"timestamp":datetime.now(tz=timezone.utc)
			,"activity":fake.text(max_nb_chars=100),"ip_address":fake.ipv4()}
		getActivityLogs=ActivityLog.objects.create(**activity)
		activity_logs.append(activity)
	return activity_logs

@pytest.fixture
def setup_filedownload():
    
	file_names=[]
	for obj in range(5):
		file_name={"unique_string" :fake.text(max_nb_chars=200)
			,"datafile":fake.file_path(depth=2,category="file",extension='xlsx')
			,"function_type" :fake.text(max_nb_chars=10)}
		getFileDownload=DownloadFile.objects.create(**file_name)
		file_names.append(file_name)
	return file_names

@pytest.fixture
def setup_getprogress(setup_saved_user):
    
	file_names=[]
	for user in Users.objects.all():
		getGetProgress=GetProgress.objects.create(user=user)		
	


