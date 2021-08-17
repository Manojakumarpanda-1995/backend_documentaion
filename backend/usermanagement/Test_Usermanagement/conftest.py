import pytest
import faker
# from usermanagement.utils.store_activity_logs import func_store_activity_logs
from django.conf import settings
from django.utils import timezone
from organization.models import *
from project.models import *
from usermanagement.models import *
from usermanagement.models import AccessManagement, Users
from usermanagement.utils.hash import (decryption, encryption,
									   generate_passwords)

refresh_lockout = getattr(settings, "LOCKOUT_COUNT_RESET_DURATION", None)
time_threshold = getattr(settings, "INCORRECT_PASSWORD_COUNT_THRESHOLD", None)
count_threshold = getattr(settings, "INCORRECT_PASSWORD_COUNT_MAX_ATTEMPTS", None)
superuser = getattr(settings, "SUPERUSER", None)
superuser_pass = getattr(settings, "SUPERUSERPASS", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)
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

@pytest.fixture(autouse=True)
def setup_superusers():

	users = [{
		"first_name": "Super",
		"last_name": " User 1",
		"name": "backend Super User 1",
		"email": "su1@kpmg.com",
		"password": generate_passwords("Password@123"),
		"token": uuid.uuid4().hex,
		"designation": "Test",
		"active": True,
		"user_verified": True,
		"reporting_manager_id": "67890",
		"reporting_manager_name": "Rohit Khandelwal",
		"reporting_manager_email": "Rohitkhandelwal@kpmg.com",
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
def setup_company(setup_superusers,setup_roles):
	company ={"name": "Administrator","created_by": 1,"updated_by": 1,}
	company["created_by"] = Users.objects.filter(id=company["created_by"])[0]
	company["updated_by"] = Users.objects.filter(id=company["updated_by"])[0]
	getCompany = Company.objects.create(**company)
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
			,"name":"Test User1","email":"test_user1@gmail.com"
			,"password":generate_passwords("Password@123"),"hashkey":uuid.uuid4().hex[:10]   	
			,"token":uuid.uuid4().hex,"designation":"Employee"
			,"active":True,"user_verified":True
			,"reporting_manager_id":"67890","reporting_manager_name":"Rohit Khandelwal"
			,"reporting_manager_email":"Rohitkhandelwal@kpmg.com"}
		,{"first_name":"Test","last_name":"User3"
			,"name":"Test User3","email":"test_user3@gmail.com"
			,"password":generate_passwords("Password@123"),"hashkey":uuid.uuid4().hex[:10]   	
			,"token":uuid.uuid4().hex,"designation":"Employee"
			,"active":True,"user_verified":True
			,"reporting_manager_id":"67890","reporting_manager_name":"Rohit Khandelwal"
			,"reporting_manager_email":"Rohitkhandelwal@kpmg.com"}
		,{"first_name":"Test","last_name":"User2"
			,"name":"Test User2","email":"test_user2@gmail.com"
			,"password":generate_passwords("Password@123"),"hashkey":uuid.uuid4().hex[:10]   	
			,"token":uuid.uuid4().hex,"designation":"Employee"
			,"active":True,"user_verified":True
			,"reporting_manager_id":"67890","reporting_manager_name":"Rohit Khandelwal"
			,"reporting_manager_email":"Rohitkhandelwal@kpmg.com"}
	]
    
    return user

@pytest.fixture
def setup_random_user():
    users=[
		{"first_name":"test","last_name":"user1","email":"testuser1@kpmg.com","active":True
   		,"user_verified":False,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
     	},
		{"first_name":"test","last_name":"user2","email":"testuser2@kpmg.com","active":True
   		,"user_verified":False,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
     	},
		{"first_name":"test","last_name":"user3","email":"testuser3@kpmg.com","active":True
   		,"user_verified":False,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
     	},
		{"first_name":"test","last_name":"user4","email":"testuser4@kpmg.com","active":False
   		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
     	}
		,{"first_name":"test","last_name":"user5","email":"testuser5@kpmg.com","active":False
   		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
     	}
		,{"first_name":"test","last_name":"user6","email":"testuser6@kpmg.com","active":False
   		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
     	}
		,{"first_name":"test","last_name":"user1","email":"testuser7@kpmg.com","active":False
   		,"user_verified":False,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
     	}
		,{"first_name":"test","last_name":"user1","email":"testuser8@kpmg.com","active":False
   		,"user_verified":False,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
     	}
	]
    return users

@pytest.fixture
def setup_saved_user():
    users=[
		{"first_name":"test","last_name":"user1","email":"testuser1@kpmg.com","active":True
   		,"user_verified":False,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
     	},
		{"first_name":"test","last_name":"user2","email":"testuser2@kpmg.com","active":True
   		,"user_verified":False,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
     	},
		{"first_name":"test","last_name":"user3","email":"testuser3@kpmg.com","active":True
   		,"user_verified":False,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
     	},
		{"first_name":"test","last_name":"user4","email":"testuser4@kpmg.com","active":False
   		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
     	}
		,{"first_name":"test","last_name":"user5","email":"testuser5@kpmg.com","active":False
   		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
     	}
		,{"first_name":"test","last_name":"user6","email":"testuser6@kpmg.com","active":False
   		,"user_verified":True,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
     	}
		,{"first_name":"test","last_name":"user1","email":"testuser7@kpmg.com","active":False
   		,"user_verified":False,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
     	}
		,{"first_name":"test","last_name":"user1","email":"testuser8@kpmg.com","active":False
   		,"user_verified":False,"password":generate_passwords("Password@123"),"token":fake.uuid4()
		   ,"hashkey":fake.uuid4()[:10],
     	}
	]
    
    for obj in users:
        getUsers=Users.objects.create(**obj)
        getAccess=AccessManagement.objects.create(name=getUsers)

