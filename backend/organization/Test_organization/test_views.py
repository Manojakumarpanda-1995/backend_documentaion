import json
import pytest
from faker import Faker 
from usermanagement.models import *
from organization.models import *
from django.conf import settings
from django.urls import reverse

fake=Faker()

class Test_create_company():
	#Test case for creating a company with all valid data.
	def test_create_company_with_valid_data(self,client):
		request=reverse("organization:create-company")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		data=json.dumps({"name": "Flipkart"
			,"address1":fake.address(),"city":fake.city(),"state":fake.state()
			,"state_pin_code":fake.postalcode()})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["message"]=="Company created successfully."
		assert response["data"]==Company.objects.count()

	#Test case for creating a company with invalid token.
	def test_create_company_with_invalid_token(self,client):
		request=reverse("organization:create-company")
		data=json.dumps({"name": fake.company()
                  ,"address1":fake.address(),"city":fake.city(),"state":fake.state()
                  ,"state_pin_code":fake.postalcode()})
		headers={"HTTP_AUTHORIZATION":fake.uuid4()}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==403
      
	#Test case for creating a company with missing/invalid parameter.
	def test_create_company_with_invalid_parameter(self,client):
		request=reverse("organization:create-company")
		data=json.dumps({"names": fake.company()
                  ,"address1":fake.address(),"city":fake.city(),"state":fake.state()
                  ,"state_pin_code":fake.postalcode()})
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
		data=json.dumps({"address1":fake.address(),"city":fake.city(),"state":fake.state()
                  ,"state_pin_code":fake.postalcode()})
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
      
	#Test case for creating a company without user authorization.
	@pytest.mark.parametrize("email",[("companyadmin@momenttext.com")
                                   ,("projectadmin@momenttext.com")
                                   ,("testuser@momenttext.com")
                                   ,("user@momenttext.com")
                                   ])
	def test_create_company_without_authorization(self,client,email):
		request=reverse("organization:create-company")
		data=json.dumps({"name": fake.company()
                  ,"address1":fake.address(),"city":fake.city(),"state":fake.state()
                  ,"state_pin_code":fake.postalcode()})
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email=email).token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Only Super User can create a company."
      
	#Test case for creating a company with existing company in db.
	@pytest.mark.parametrize("company_name",[("Amazon")
        ,("Google"),("Gmail"),("Administrator"),("Tesla"),("Infosys"),("Tata")
                                   ])
	def test_create_company_with_existing_company(self,client,company_name):
		request=reverse("organization:create-company")
		data=json.dumps({"name": company_name
                  ,"address1":fake.address(),"city":fake.city(),"state":fake.state()
                  ,"state_pin_code":fake.postalcode()})
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Company name already exists"
      		
class Test_get_company():
    
    #Test case for getting company data with all valid parameters
	def test_get_company_with_valid_data(self,client):
		request=reverse("organization:get-company")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		data=json.dumps({"client_id":1})
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["message"]=="Company fetched successfully."
		getCompany=Company.objects.get(id=1)
		assert response["data"]["name"]== "Administrator"
		assert response["data"]["id"]==getCompany.id
		assert response["data"]["name"]==getCompany.name
		assert response["data"]["city"]==getCompany.city
		assert response["data"]["state"]==getCompany.state
		assert response["data"]["country"]==getCompany.country
		assert response["data"]["partner_name"]==getCompany.partner_name
		assert response["data"]["state_pin_code"]==getCompany.state_pin_code
		assert response["data"]["active"]==True
		assert response["data"]["created_at"]==(getCompany.created_at).strftime("%d-%m-%Y")
		assert response["data"]["created_by_id"]== 1
		assert response["data"]["updated_at"]==(getCompany.updated_at).strftime("%d-%m-%Y")
		assert response["data"]["updated_by_id"]== 1
  
    #Test case for getting company data with invalid client_id
	@pytest.mark.parametrize("client_id",[(15),(25),(35),(45),(55)])
	def test_get_company_with_invalid_client_id(self,client,client_id):
		request=reverse("organization:get-company")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		data=json.dumps({"client_id":client_id})
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="No company found in database."
  
    #Test case for getting company data with all company
	@pytest.mark.parametrize("company,client_id",[("Google",2)
				,("Gmail",3),("Amazon",4),("Tesla",5),("Infosys",6),("Tata",7)]) 			
	def test_get_company_with_all_company(self,client,company,client_id):
		request=reverse("organization:get-company")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		data=json.dumps({"client_id":client_id})
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["message"]=="Company fetched successfully."
		getCompany=Company.objects.get(id=client_id)
		assert response["data"]["name"]==company
		assert response["data"]["id"]==getCompany.id
		assert response["data"]["name"]==getCompany.name
		assert response["data"]["city"]==getCompany.city
		assert response["data"]["state"]==getCompany.state
		assert response["data"]["country"]==getCompany.country
		assert response["data"]["partner_name"]==getCompany.partner_name
		assert response["data"]["state_pin_code"]==getCompany.state_pin_code
		assert response["data"]["active"]==True
		assert response["data"]["created_at"]==(getCompany.created_at).strftime("%d-%m-%Y")
		assert response["data"]["created_by_id"]== 1
		assert response["data"]["updated_at"]==(getCompany.updated_at).strftime("%d-%m-%Y")
		assert response["data"]["updated_by_id"]== 1
  
	#Test case for get company with missing/invalid parameter.
	def test_get_company_with_invalid_parameter(self,client):
		request=reverse("organization:get-company")
		data=json.dumps({"client_ids":2})
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
		data=json.dumps({"city":fake.city()})
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
  
	#Test case for get company with invalid token.
	def test_get_company_with_invalid_token(self,client):
		request=reverse("organization:get-company")
		data=json.dumps({"client_id":3})
		headers={"HTTP_AUTHORIZATION":fake.uuid4()}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==403
    
	#Test case for get company without user authorization.
	@pytest.mark.parametrize("email",[("projectadmin@momenttext.com")
                                   ,("testuser@momenttext.com")
                                   ,("user@momenttext.com")
                                   ])
	def test_get_company_without_authorization(self,client,email):
		request=reverse("organization:get-company")
		data=json.dumps({"client_id":2})
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email=email).token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Only SuperUser can fetch the company."
     			
class Test_delete_company():
    
    #Test case for deleteing company data with all valid parameters
	def test_delete_company_with_valid_data(self,client):
		request=reverse("organization:delete-company")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		data=json.dumps({"client_id":1,"status":False})
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["message"]=="Company deleted successfully."
		getCompany=Company.objects.get(id=1)
		assert getCompany.active==False
  
    #Test case for deleteing company data with invalid client_id
	@pytest.mark.parametrize("client_id",[(15),(25),(35),(55),(45)])
	def test_delete_company_with_invalid_client_id(self,client,client_id):
		request=reverse("organization:delete-company")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		data=json.dumps({"client_id":client_id,"status":True})
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Company with provided ID doesn't exist."
  
    #Test case for deleteing company data with all company
	@pytest.mark.parametrize("status,client_id",[(False,2)
				,(True,3),(False,4),(True,5),(False,6),(True,7)]) 			
	def test_delete_company_with_all_company(self,client,status,client_id):
		request=reverse("organization:delete-company")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		data=json.dumps({"client_id":client_id,"status":status})
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		if status:
			assert response["message"]=="Company activated successfully."
		else:
			assert response["message"]=="Company deleted successfully."
		getCompany=Company.objects.get(id=client_id)
		assert getCompany.active==status
		  
	#Test case for delete company with missing/invalid parameter.
	def test_delete_company_with_invalid_parameter(self,client):
		request=reverse("organization:delete-company")
		data=json.dumps({"client_ids":2})
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
		data=json.dumps({"client_id":2})
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
  
	#Test case for delete company with invalid token.
	def test_delete_company_with_invalid_token(self,client):
		request=reverse("organization:delete-company")
		data=json.dumps({"client_id":3})
		headers={"HTTP_AUTHORIZATION":fake.uuid4()}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==403
    
	#Test case for delete company without user authorization.
	@pytest.mark.parametrize("email",[("companyadmin@momenttext.com")
                                   ,("projectadmin@momenttext.com")
                                   ,("testuser@momenttext.com")
                                   ,("user@momenttext.com")
                                   ])
	def test_delete_company_without_authorization(self,client,email):
		request=reverse("organization:delete-company")
		data=json.dumps({"client_id":2})
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email=email).token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="You are not authorized to delete company."

	#Test case for re activate the company
	def test_delete_company_with_activate(self,client):
		request=reverse("organization:delete-company")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		data=json.dumps({"client_id":3,"status":True})
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["message"]=="Company activated successfully."
		assert Company.objects.get(id=3).active==True		
  				
class Test_list_company():
    
     #Test case for listing company data with all valid parameters
	def test_list_company_with_valid_data(self,client,setup_list_company):
		request=reverse("organization:list-company")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		data=json.dumps({"client_id":2})
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["message"]=="List companies successfully."
		getCompany=Company.objects.all().exclude(id=1,name="Administrator")
		assert len(response["data"])==len(getCompany)
		for x in range(len(getCompany)):
			company=getCompany[x]
			getCompanyAdmin = UserCompanyRole.objects.filter(company=company
										, role__role_name="COMPANY-ADMIN"
										, isActive=True, user__active=True)
			if len(getCompanyAdmin) > 0:
				getCompanyAdmin = getCompanyAdmin[0]
				company_admin = getCompanyAdmin.user.email
				company_admin_id = getCompanyAdmin.user.id
			else:
				company_admin = None
				company_admin_id = None
					
			assert response["data"][x]["id"]==company.id
			assert response["data"][x]["name"]==company.name
			assert response["data"][x]["partner_name"]==company.partner_name
			assert response["data"][x]["status"]==company.active
			assert response["data"][x]["company_admin"]==company_admin
			assert response["data"][x]["company_admin_id"]==company_admin_id
			assert response["data"][x]["isEditable"]==True
			assert response["data"][x]["isShow"]==True
    
    #Test case for listing company data with all company as a company admin role			
	def test_list_company_with_company_admin(self,client,setup_list_company):
		request=reverse("organization:list-company")
		getUsers=Users.objects.get(email="companyadmin@momenttext.com")
		data=json.dumps({})
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["message"]=="List companies successfully."
		getCompany=Company.objects.all().exclude(id=1,name="Administrator")
		assert len(response["data"])==len(getCompany)
		for x in range(len(getCompany)):
			assert response["data"][x]["isEditable"]==False
  	
	#Test case for list company with invalid token.
	def test_list_company_with_invalid_token(self,client):
		request=reverse("organization:list-company")
		data=json.dumps({"client_id":3})
		headers={"HTTP_AUTHORIZATION":fake.uuid4()}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==403
    
	#Test case for list company without user authorization.
	@pytest.mark.parametrize("email",[("testuser@momenttext.com"),("user@momenttext.com")])
	def test_list_company_without_authorization(self,client,email):
		request=reverse("organization:list-company")
		data=json.dumps({"client_id":2})
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email=email).token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="You are not authorized to list companies."
    
    #Test case for listing company data with all company as a project-admin role 
	def test_list_company_with_project_admin(self,client):
		getUsers=Users.objects.get(email="projectadmin@momenttext.com")
		request=reverse("organization:list-company")
		data=json.dumps({})
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["message"]=="List companies successfully."
		getCompany=Company.objects.all().exclude(id=1,name="Administrator")
		getUserCompanyRole=len(UserCompanyRole.objects.filter(user=getUsers,role__id=3))
		assert len(response["data"])==getUserCompanyRole
		for x in range(getUserCompanyRole):
			assert response["data"][x]["isEditable"]==False
				
class Test_list_company_byemail():
    
    #Test case for list company by email with all valid info with user as superuser
	def test_list_company_byemail_with_user_as_superuser(self,client):
		request=reverse("organization:list-company-byemail")
		getUser=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUser.token}
		data=json.dumps({"email":"su1@momenttext.com"})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		response["statuscode"]==200
		assert len(response["data"])==1
		assert response["data"][0]["id"]==1
		assert response["data"][0]["name"]=='Administrator'
		assert response["data"][0]["role"]=='SUPER-USER'
		response["message"]=="List companies successfull."
  
    #Test case for list company by email with all valid info with user as superuser
	def test_list_company_byemail_with_user_as_superuser(self,client):
		request=reverse("organization:list-company-byemail")
		getUser=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUser.token}
		data=json.dumps({"email":"su1@momenttext.com"})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		response["statuscode"]==200
		assert len(response["data"])==1
		assert response["data"][0]["id"]==1
		assert response["data"][0]["name"]=='Administrator'
		assert response["data"][0]["role"]=='SUPER-USER'
		response["message"]=="List companies successfull."

	#Test case for list company byemail with invalid token.
	def test_list_company_with_invalid_token(self,client):
		request=reverse("organization:list-company-byemail")
		data=json.dumps({"client_id":3})
		headers={"HTTP_AUTHORIZATION":fake.uuid4()}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==403

	#Test case for list company byemail with missing/invalid parameter.
	def test_list_company_byemail_with_invalid_parameter(self,client):
		request=reverse("organization:list-company-byemail")
		data=json.dumps({"emails":"companyadmin@momenttext.com"})
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
		data=json.dumps({"client_id":2})
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500

	# Test case for list company byemail with all user roles
	@pytest.mark.parametrize("email,role",[("companyadmin@momenttext.com","COMPANY-ADMIN")
                                   ,("projectadmin@momenttext.com","PROJECT-ADMIN")
                                   ,("testuser@momenttext.com","USER"),("user@momenttext.com","USER")
                                   ])
	def test_list_company_byemail_with_all_roles(self,client,email,role):
		request=reverse("organization:list-company-byemail")
		getUser=Users.objects.get(email=email)
		headers={"HTTP_AUTHORIZATION":getUser.token}
		data=json.dumps({"email":email})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		getUserCompanyRole=UserCompanyRole.objects.filter(user__email=email,role__role_name=role)
		response["statuscode"]==200
		assert len(response["data"])==len(getUserCompanyRole)
		for x in range(len(getUserCompanyRole)):
			assert response["data"][x]["id"]==getUserCompanyRole[x].company.id
			assert response["data"][x]["name"]==getUserCompanyRole[x].company.name
			assert response["data"][x]["role"]==role
		response["message"]=="List companies successfull."

	# Test case for list company byemail with all user
	@pytest.mark.parametrize("email",[("testuser1@momenttext.com")
									,("testuser2@momenttext.com")
									,("testuser3@momenttext.com")
									,("testuser4@momenttext.com")
									,("testuser5@momenttext.com")
									,("testuser6@momenttext.com")
                                   ])
	def test_list_company_byemail_with_all_user(self,client,email,setup_usercompany_role):
		request=reverse("organization:list-company-byemail")
		getUser=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUser.token}
		data=json.dumps({"email":email})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		print("Responses==>",response)
		# getUserCompanyRole=UserCompanyRole.objects.filter(user__email=email,role__role_name=role)
		# response["statuscode"]==200
		# assert len(response["data"])==len(getUserCompanyRole)
		# for x in range(len(getUserCompanyRole)):
		# 	assert response["data"][x]["id"]==getUserCompanyRole[x].company.id
		# 	assert response["data"][x]["name"]==getUserCompanyRole[x].company.name
		# 	assert response["data"][x]["role"]==role
		response["message"]=="List companies successfull."


 
@pytest.mark.xfail				
class Test_edit_company():
	def test_edit_company(self,*args, **kwargs):
		request=reverse("organization:edit-company")
		headers={"HTTP_AUTHORIZATION":""}

@pytest.mark.xfail				
class Test_get_company_info():
	def test_get_company_info(self,*args, **kwargs):
		request=reverse("organization:get-company-info")
		headers={"HTTP_AUTHORIZATION":""}

@pytest.mark.xfail				
class Test_edit_company_info():
	def test_edit_company_info(self,*args, **kwargs):
		request=reverse("organization:edit-company-info")
		headers={"HTTP_AUTHORIZATION":""}

@pytest.mark.xfail				
class Test_list_users():
	def test_list_users(self):
		request=reverse("organization:list-users")
		headers={"HTTP_AUTHORIZATION":""}
		
@pytest.mark.xfail				
class Test_create_usercompanyrole():
	def test_create_usercompanyrole(self,*args, **kwargs):
		request=reverse("organization:create-usercompanyrole")
		headers={"HTTP_AUTHORIZATION":""}
				
@pytest.mark.xfail				
class Test_deactivate_usercompanyrole():
	def test_deactivate_usercompanyrole(self,*args, **kwargs):
		request=reverse("organization:deactivate-usercompanyrole")
		headers={"HTTP_AUTHORIZATION":""}
		
  
		
   