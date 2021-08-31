from conftest import setup_create_usercompanyrole_with_existing_companyrole
import json
import pytest
import random
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
		data=json.dumps({"name":fake.company(),"country":fake.country()
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
		data=json.dumps({"name": fake.company(),"country":fake.country()
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
		data=json.dumps({"names": fake.company(),"country":fake.country()
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
		data=json.dumps({"name": fake.company(),"country":fake.country()
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
		data=json.dumps({"name": company_name,"country":fake.country()
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
		data=json.dumps({"city":fake.company()})
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
		getUserCompanyRole= UserCompanyRole.objects.filter(user__email=email,
										# company=company.company,
										user__active=True,
										company__active=True, 
										role__active=True, 
										isActive=True)
		response["statuscode"]==200
		assert len(response["data"])==len(getUserCompanyRole)
		for x in range(len(getUserCompanyRole)):
			assert response["data"][x]["id"]==getUserCompanyRole[x].company.id
			assert response["data"][x]["name"]==getUserCompanyRole[x].company.name
			assert response["data"][x]["role"]==getUserCompanyRole[x].role.role_name
		response["message"]=="List companies successfull."
 				
class Test_edit_company():
    
    #Test case for editing a company with all valid data.
	def test_edit_company_with_valid_data(self,client):
		request=reverse("organization:edit-company")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		getCompany=Company.objects.get(id=2)
		assert getCompany.name=="Google"
		assert getCompany.city is None
		assert getCompany.address1 is None
		assert getCompany.state is None
		assert getCompany.state_pin_code is None
		data={"client_id":2,"name":fake.company(),"country":fake.country(),"partner_name":fake.name()
			,"address1":fake.address(),"city":fake.city(),"state":fake.state()
			,"state_pin_code":fake.postalcode()}
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["message"]=="Company data updated successfully."
		getCompany=Company.objects.get(id=2)
		assert getCompany.name==data["name"]
		assert getCompany.city==data["city"]
		assert getCompany.address1==data["address1"]
		assert getCompany.state==data["state"]
		assert getCompany.state_pin_code==data["state_pin_code"]
		assert getCompany.country==data["country"]
		assert getCompany.partner_name==data["partner_name"]

	#Test case for editing a company with invalid token.
	def test_edit_company_with_invalid_token(self,client):
		request=reverse("organization:edit-company")
		data=json.dumps({"client_id":2,"name":fake.company(),"country":fake.country()
			,"address1":fake.address(),"city":fake.city(),"state":fake.state()
			,"state_pin_code":fake.postalcode()})
		headers={"HTTP_AUTHORIZATION":fake.uuid4()}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==403
      
	#Test case for creating a company with missing/invalid parameter.
	def test_edit_company_with_invalid_parameter(self,client):
		request=reverse("organization:edit-company")
		data=json.dumps({"client_ids":2,"name":fake.company(),"country":fake.country()
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
      
	#Test case for editing a company without user authorization.
	@pytest.mark.parametrize("email",[("projectadmin@momenttext.com")
                                   ,("testuser@momenttext.com")
                                   ,("user@momenttext.com")
                                   ])
	def test_edit_company_without_authorization(self,client,email):
		request=reverse("organization:edit-company")
		data=json.dumps({"client_id":2,"name":fake.company(),"country":fake.country()
			,"address1":fake.address(),"city":fake.city(),"state":fake.state()
			,"state_pin_code":fake.postalcode()})
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email=email).token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="You are not authorized to edit company details."
      
	#Test case for editing a company with invalid client_id.
	@pytest.mark.parametrize("client_id",[(30),(40),(50),(60),(15),(70)])
	def test_edit_company_with_existing_company(self,client,client_id):
		request=reverse("organization:edit-company")
		data=json.dumps({"client_id":client_id
                  ,"address1":fake.address(),"city":fake.city(),"state":fake.state()
                  ,"state_pin_code":fake.postalcode()})
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Company with provided ID doesn't exist."
    
	#Test case for editing a company with user of different companies 
	@pytest.mark.parametrize("client_id",[(3),(4),(5),(6),(1),(7)])
	def test_edit_company(self,client,client_id):
		request=reverse("organization:edit-company")
		getUsers=Users.objects.get(email="companyadmin@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		data={"client_id":client_id,"name":fake.company(),"partner_name":fake.name()
                  ,"address1":fake.address(),"city":fake.city(),"state":fake.state()
                  ,"state_pin_code":fake.postalcode(),"country":fake.country()}
		getCompany=Company.objects.get(id=client_id)
		assert getCompany.state_pin_code is None
		assert getCompany.name is not None
		assert getCompany.city is None
		assert getCompany.address1 is None
		assert getCompany.state is None
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["message"]=="Company data updated successfully."
		getCompany=Company.objects.get(id=client_id)
		assert getCompany.name==data["name"]
		assert getCompany.city==data["city"]
		assert getCompany.address1==data["address1"]
		assert getCompany.state==data["state"]
		assert getCompany.state_pin_code==data["state_pin_code"]
		assert getCompany.country==data["country"]
		assert getCompany.partner_name==data["partner_name"]
  				
class Test_get_company_info():
    
     #Test case for getting company info data with all valid parameters
	def test_get_company_info_with_valid_data(self,client):
		request=reverse("organization:get-company-info")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		data=json.dumps({"client_id":2})
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["message"]=="Company Information fetched successfully."
		getCompany=Company.objects.get(id=2)
		getCompanyInfo=CompanyInfo.objects.get(company=getCompany)
		assert len(Company.objects.all())==CompanyInfo.objects.count()
		assert response["data"]["id"]==getCompanyInfo.id
		assert response["data"]["company_id"]==getCompany.id
		assert response["data"]["logo"] is not None
		assert response["data"]["corporate_type"]==getCompanyInfo.corporate_type
		assert response["data"]["number_of_emploies"]==getCompanyInfo.number_of_emploies
		assert response["data"]["type"]==getCompanyInfo.type
		assert response["data"]["links"]==getCompanyInfo.links
		assert response["data"]["about"]==getCompanyInfo.about
		assert len(response["data"]["about"])<=500
		assert response["data"]["active"]==True
		assert response["data"]["created_at"]==getCompanyInfo.created_at.strftime("%d-%m-%Y")
		assert response["data"]["updated_at"]==getCompanyInfo.updated_at.strftime("%d-%m-%Y")
		assert response["data"]["created_by_id"]==1
		assert response["data"]["updated_by_id"]==1
		assert response["data"]["name"]==getCompany.name
		assert response["data"]["city"] is None
		assert response["data"]["state"] is None
		assert response["data"]["country"] is None
		assert response["data"]["state_pin_code"] is None
  
    #Test case for getting company info data with invalid client_id
	@pytest.mark.parametrize("client_id",[(15),(25),(35),(45),(55)])
	def test_get_company_info_with_invalid_client_id(self,client,client_id):
		request=reverse("organization:get-company-info")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		data=json.dumps({"client_id":client_id})
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="No Company Information found in database."
  
    #Test case for getting company info data with all company
	@pytest.mark.parametrize("company,client_id",[("Google",2)
				,("Gmail",3),("Amazon",4),("Tesla",5),("Infosys",6),("Tata",7)]) 			
	def test_get_company_info_with_all_company(self,client,company,client_id):
		request=reverse("organization:get-company-info")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		data=json.dumps({"client_id":client_id})
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["message"]=="Company Information fetched successfully."
		getCompany=Company.objects.get(id=client_id)
		getCompanyInfo=CompanyInfo.objects.get(company=getCompany)
		assert len(Company.objects.all())==CompanyInfo.objects.count()
		assert response["data"]["id"]==getCompanyInfo.id
		assert response["data"]["company_id"]==getCompany.id
		assert response["data"]["logo"] is not None
		assert response["data"]["corporate_type"]==getCompanyInfo.corporate_type
		assert response["data"]["number_of_emploies"]==getCompanyInfo.number_of_emploies
		assert response["data"]["type"]==getCompanyInfo.type
		assert response["data"]["links"]==getCompanyInfo.links
		assert response["data"]["about"]==getCompanyInfo.about
		assert len(response["data"]["about"])<=500
		assert response["data"]["active"]==True
		assert response["data"]["created_at"]==getCompanyInfo.created_at.strftime("%d-%m-%Y")
		assert response["data"]["updated_at"]==getCompanyInfo.updated_at.strftime("%d-%m-%Y")
		assert response["data"]["created_by_id"]==1
		assert response["data"]["updated_by_id"]==1
		assert response["data"]["name"]==company
		assert response["data"]["city"] is None
		assert response["data"]["state"] is None
		assert response["data"]["country"] is None
		assert response["data"]["state_pin_code"] is None
  
	#Test case for get company info with missing/invalid parameter.
	def test_get_company_info_with_invalid_parameter(self,client):
		request=reverse("organization:get-company-info")
		data=json.dumps({"client_ids":2})
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
		data=json.dumps({"name":fake.company()})
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
  
	#Test case for get company info with invalid token.
	def test_get_company_info_with_invalid_token(self,client):
		request=reverse("organization:get-company-info")
		data=json.dumps({"client_id":3})
		headers={"HTTP_AUTHORIZATION":fake.uuid4()}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==403
    
	#Test case for get company info without user authorization.
	@pytest.mark.parametrize("email",[("projectadmin@momenttext.com")
                                   ,("testuser@momenttext.com")
                                   ,("user@momenttext.com")
                                   ])
	def test_get_company_info_without_authorization(self,client,email):
		request=reverse("organization:get-company-info")
		data=json.dumps({"client_id":2})
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email=email).token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Only SuperUser can fetch the Company Information."
    
	#Test case for the get company info where only company data is there but not extra info
	@pytest.mark.parametrize("email",[("companyadmin@momenttext.com")])
	def test_get_company_info(self,client,email,setup_test_company):
		companies=setup_test_company
		request=reverse("organization:get-company-info")
		for company in companies:
			getCompany=Company.objects.get(name=company["name"])
			data=json.dumps({"client_id":getCompany.id})
			headers={"HTTP_AUTHORIZATION":Users.objects.get(email=email).token}
			response=client.post(request,data=data,content_type="application/json",**headers)
			assert response.status_code==200
			response=response.json()
			assert response["statuscode"]==200
			assert response["message"]=="Company Information fetched successfully."
			assert response["data"]["id"]==getCompany.id
			assert response["data"]["name"]==company["name"]
			assert response["data"]["address1"]==company["address1"]
			assert response["data"]["city"]==company["city"]
			assert response["data"]["state"]==company["state"]
			assert response["data"]["country"]==company["country"]
			assert response["data"]["partner_name"]==company["partner_name"]
			assert response["data"]["state_pin_code"]==company["state_pin_code"]
			assert response["data"]["active"]==company["active"]
			assert response["data"]["created_by_id"]==1
			assert response["data"]["updated_by_id"]==1
				
class Test_edit_company_info():
    
    #Test case for editing a company information with all valid data.
	def test_edit_company_info_with_valid_data(self,client):
		request=reverse("organization:edit-company-info")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		getCompany=Company.objects.get(id=2)
		assert getCompany.name=="Google"
		assert getCompany.city is None
		assert getCompany.address1 is None
		assert getCompany.state is None
		assert getCompany.state_pin_code is None
		data={"client_id":[2],"name":[fake.company()],"country":[fake.country()],"partner_name":[fake.name()]
		,"address1":[fake.address()],"city":[fake.city()]
		,"state":[fake.state()],"state_pin_code":[fake.postalcode()]
		#company info data
		,"logo":[fake.image_url()],"corporate_type":["Insurance"],"number_of_emploies":[fake.building_number()]
		,"type":["Finance"],"links":[fake.url()],"about":[fake.text(max_nb_chars=500)],"active":[fake.boolean()]
		}
		# response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		response=client.post(request,data=json.dumps(data),content_type="application/json"
                       ,body="form-data",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["message"]=="Company information data updated successfully."
		getCompany=Company.objects.get(id=2)
		getCompanyInfo=CompanyInfo.objects.get(company=getCompany)
		assert getCompany.name==data["name"][0]
		assert getCompany.city==data["city"][0]
		assert getCompany.address1==data["address1"][0]
		assert getCompany.state==data["state"][0]
		assert getCompany.state_pin_code==data["state_pin_code"][0]
		assert getCompany.country==data["country"][0]
		assert getCompany.partner_name==data["partner_name"][0]
		assert getCompanyInfo.logo == data["logo"][0]
		assert getCompanyInfo.corporate_type =="Insurance"
		assert getCompanyInfo.number_of_emploies==data["number_of_emploies"][0]
		assert getCompanyInfo.type=="Finance"
		assert getCompanyInfo.links ==data["links"][0]
		assert getCompanyInfo.about==data["about"][0]
		assert getCompanyInfo.active==data["active"][0]
  
    #Test case for editing all company information with all valid data.
	@pytest.mark.parametrize("client_id",[(3),(4),(5),(6)])
	def test_edit_all_company_info_with_valid_data(self,client,client_id):
		request=reverse("organization:edit-company-info")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		getCompany=Company.objects.get(id=client_id)
		assert getCompany.city is None
		assert getCompany.address1 is None
		assert getCompany.state is None
		assert getCompany.state_pin_code is None
		data={"client_id":[client_id],"name":[fake.company()],"country":[fake.country()]
        ,"partner_name":[fake.name()],"address1":[fake.address()],"city":[fake.city()]
		,"state":[fake.state()],"state_pin_code":[fake.postalcode()]
		#company info data
		,"logo":[fake.image_url()],"corporate_type":["Insurance"],"number_of_emploies":[fake.building_number()]
		,"type":["Finance"],"links":[fake.url()],"about":[fake.text(max_nb_chars=500)],"active":[fake.boolean()]
		}
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["message"]=="Company information data updated successfully."
		getCompany=Company.objects.get(id=client_id)
		getCompanyInfo=CompanyInfo.objects.get(company=getCompany)
		assert getCompany.name==data["name"][0]
		assert getCompany.city==data["city"][0]
		assert getCompany.address1==data["address1"][0]
		assert getCompany.state==data["state"][0]
		assert getCompany.state_pin_code==data["state_pin_code"][0]
		assert getCompany.country==data["country"][0]
		assert getCompany.partner_name==data["partner_name"][0]
		assert getCompanyInfo.logo == data["logo"][0]
		assert getCompanyInfo.corporate_type =="Insurance"
		assert getCompanyInfo.number_of_emploies==data["number_of_emploies"][0]
		assert getCompanyInfo.type=="Finance"
		assert getCompanyInfo.links ==data["links"][0]
		assert getCompanyInfo.about==data["about"][0]
		assert getCompanyInfo.active==data["active"][0]

	#Test case for editing a company information with invalid token.
	def test_edit_company_info_with_invalid_token(self,client):
		request=reverse("organization:edit-company-info")
		data={"client_id":[4],"name":[fake.company()],"country":[fake.country()],"partner_name":[fake.name()]
		,"address1":[fake.address()],"city":[fake.city()],"state":[fake.state()],"state_pin_code":[fake.postalcode()]
		#company info data
		,"logo":[fake.image_url()],"corporate_type":["Insurance"],"number_of_emploies":[fake.building_number()]
		,"type":["Finance"],"links":[fake.url()],"about":[fake.text(max_nb_chars=500)],"active":[fake.boolean()]
		}
		headers={"HTTP_AUTHORIZATION":fake.uuid4()}
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==403
      
	#Test case for editing company information with missing/invalid parameter.
	def test_edit_company_info_with_invalid_parameter(self,client):
		request=reverse("organization:edit-company-info")
		data={"client_ids":[5],"name":[fake.company()],"country":[fake.country()]
        ,"partner_name":[fake.name()],"address1":[fake.address()],"city":[fake.city()]
		,"state":[fake.state()],"state_pin_code":[fake.postalcode()]
		#company info data
		,"logo":[fake.image_url()],"corporate_type":"Insurance","number_of_emploies":[fake.building_number()]
		,"type":["Finance"],"links":[fake.url()],"about":[fake.text(max_nb_chars=500)],"active":[fake.boolean()]
		}
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
		data={"name":[fake.company()],"country":[fake.country()],"partner_name":[fake.name()]
		,"address1":[fake.address()],"city":[fake.city()]
		,"state":[fake.state()],"state_pin_code":[fake.postalcode()]
		#company info data
		,"logo":[fake.image_url()],"corporate_type":["Insurance"],"number_of_emploies":[fake.building_number()]
		,"type":["Finance"],"links":[fake.url()],"about":[fake.text(max_nb_chars=500)],"active":[fake.boolean()]
		}
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
      
	#Test case for editing a company information without user authorization.
	@pytest.mark.parametrize("email",[("projectadmin@momenttext.com")
                                   ,("testuser@momenttext.com")
                                   ,("user@momenttext.com")
                                   ])
	def test_edit_company_info_without_authorization(self,client,email):
		request=reverse("organization:edit-company-info")
		data={"client_id":[3],"name":[fake.company()],"country":[fake.country()]
        ,"partner_name":[fake.name()],"address1":[fake.address()],"city":[fake.city()]
		,"state":[fake.state()],"state_pin_code":[fake.postalcode()]
		#company info data
		,"logo":[fake.image_url()],"corporate_type":["Insurance"],"number_of_emploies":[fake.building_number()]
		,"type":["Finance"],"links":[fake.url()],"about":[fake.text(max_nb_chars=500)],"active":[fake.boolean()]
		}
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email=email).token}
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="You are not authorized to edit company information details."
      
	#Test case for editing a company information with invalid client_id.
	@pytest.mark.parametrize("client_id",[(30),(40),(50),(60),(15),(70)])
	def test_edit_company_info_with_invalid_company_id(self,client,client_id):
		request=reverse("organization:edit-company-info")
		data={"client_id":[client_id],"name":[fake.company()],"country":[fake.country()]
        ,"partner_name":[fake.name()],"address1":[fake.address()],"city":[fake.city()]
		,"state":[fake.state()],"state_pin_code":[fake.postalcode()]
		#company info data
		,"logo":[fake.image_url()],"corporate_type":["Insurance"],"number_of_emploies":[fake.building_number()]
		,"type":["Finance"],"links":[fake.url()],"about":[fake.text(max_nb_chars=500)],"active":[fake.boolean()]
		}
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Company with provided ID doesn't exist."
    
	#Test case for editing a company information with user of different companies 
	@pytest.mark.parametrize("client_id",[(3),(4),(5),(6),(1),(7)])
	def test_edit_company_info(self,client,client_id):
		request=reverse("organization:edit-company-info")
		getUsers=Users.objects.get(email="companyadmin@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		data={"client_id":[client_id],"name":[fake.company()],"country":[fake.country()]
        ,"partner_name":[fake.name()],"address1":[fake.address()],"city":[fake.city()]
		,"state":[fake.state()],"state_pin_code":[fake.postalcode()]
		#company info data
		,"logo":[fake.image_url()],"corporate_type":["Travel Insurance"],"number_of_emploies":[fake.building_number()]
		,"type":["Tour & Travel"],"links":[fake.url()],"about":[fake.text(max_nb_chars=500)],"active":[fake.boolean()]
		}
		getCompany=Company.objects.get(id=client_id)
		assert getCompany.state_pin_code is None
		assert getCompany.name is not None
		assert getCompany.city is None
		assert getCompany.address1 is None
		assert getCompany.state is None
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["message"]=="Company information data updated successfully."
		getCompany=Company.objects.get(id=client_id)
		getCompanyInfo=CompanyInfo.objects.get(company=getCompany)
		assert getCompany.name==data["name"][0]
		assert getCompany.city==data["city"][0]
		assert getCompany.address1==data["address1"][0]
		assert getCompany.state==data["state"][0]
		assert getCompany.state_pin_code==data["state_pin_code"][0]
		assert getCompany.country==data["country"][0]
		assert getCompany.partner_name==data["partner_name"][0]
		assert getCompanyInfo.logo == data["logo"][0]
		assert getCompanyInfo.corporate_type =="Travel Insurance"
		assert getCompanyInfo.number_of_emploies==data["number_of_emploies"][0]
		assert getCompanyInfo.type=="Tour & Travel"
		assert getCompanyInfo.links ==data["links"][0]
		assert getCompanyInfo.about==data["about"][0]
		assert getCompanyInfo.active==data["active"][0]
  	
	#Test case for edit company info with user whose roles are not assined
	@pytest.mark.parametrize("email",[("testuser1@momenttext.com"),("testuser2@momenttext.com")
							,("testuser3@momenttext.com")])
	def test_edit_company_info_without_user_role(self,client,email,setup_user_for_new_password):
		request=reverse("organization:edit-company-info")
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email=email).token}
		data={"client_id":[4],"name":[fake.company()],"country":[fake.country()],"partner_name":[fake.name()]
		,"address1":[fake.address()],"city":[fake.city()]
		,"state":[fake.state()],"state_pin_code":[fake.postalcode()]
		#company info data
		,"logo":[fake.image_url()],"corporate_type":["Travel Insurance"],"number_of_emploies":[fake.building_number()]
		,"type":["Tour & Travel"],"links":[fake.url()],"about":[fake.text(max_nb_chars=500)],"active":[fake.boolean()]
		}
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["message"]=="You are not authorized to edit company information details."
		assert response["statuscode"]== 400
                                   				
class Test_list_users():
    #Test case for list users with all valid data.
	def test_list_users_with_valid_data(self,client):
		request=reverse("organization:list-users")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		data={"company_id":2}
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		getUserRole=UserCompanyRole.objects.exclude(user__email="su1@momenttext.com")
		assert len(response["data"])==len(getUserRole)
		assert response["message"]=="Users listed successfully."
		for x in range(len(getUserRole)):
			assert response["data"][x]["id"]==getUserRole[x].user.id
			assert response["data"][x]["name"]==getUserRole[x].user.name
			assert response["data"][x][ "email"]==getUserRole[x].user.email
			assert response["data"][x]["status"]==getUserRole[x].user.active

    #Test case for list users with all company data.
	@pytest.mark.parametrize("company_id",[(3),(4),(5),(6),(7),(8)])
	def test_list_users_with_all_company_id(self,client,company_id):
		request=reverse("organization:list-users")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		data={"company_id":company_id}
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["message"]=="Users listed successfully."
		getUserRole=UserCompanyRole.objects.exclude(user__email="su1@momenttext.com")
		assert len(response["data"])==len(getUserRole)
		assert response["message"]=="Users listed successfully."
		for x in range(len(getUserRole)):
			assert response["data"][x]["id"]==getUserRole[x].user.id
			assert response["data"][x]["name"]==getUserRole[x].user.name
			assert response["data"][x][ "email"]==getUserRole[x].user.email
			assert response["data"][x]["status"]==getUserRole[x].user.active
		
	#Test case for list users with invalid token.
	def test_list_users_with_invalid_token(self,client):
		request=reverse("organization:list-users")
		data={"company_id":4}
		headers={"HTTP_AUTHORIZATION":fake.uuid4()}
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==403
      
	#Test case for list users with missing/invalid parameter.
	def test_list_users_with_invalid_parameter(self,client):
		request=reverse("organization:list-users")
		data={"client_ids":5}
		getUsers=Users.objects.get(email="companyadmin@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
		data={"name":fake.company()}
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
      
	#Test case for list users without user authorization.
	@pytest.mark.parametrize("email",[("testuser@momenttext.com")
                                   ,("user@momenttext.com")
                                   ])
	def test_list_users_without_authorization(self,client,email):
		request=reverse("organization:list-users")
		data={"company_id":3}
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email=email).token}
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="You are not authorized to list users."
      
	#Test case for list users with user as company&project-admin 
	@pytest.mark.parametrize("email",[("companyadmin@momenttext.com"),("projectadmin@momenttext.com")])
	def test_list_users_without_superuser_role(self,client,email):
		request=reverse("organization:list-users")
		getUsers=Users.objects.get(email=email)
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		getCompany=Company.objects.get(name="Microsoft")
		data={"company_id":getCompany.id}
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		getUserRole=UserCompanyRole.objects.exclude(user__email="su1@momenttext.com")
		if email=="projectadmin@momenttext.com":
			assert response["statuscode"]==200
			assert response["message"]=="Users listed successfully."
		else:
			assert len(response["data"])==len(getUserRole)
			for x in range(len(getUserRole)):
				assert response["data"][x]["id"]==getUserRole[x].user.id
				assert response["data"][x]["name"]==getUserRole[x].user.name
				assert response["data"][x][ "email"]==getUserRole[x].user.email
				assert response["data"][x]["status"]==getUserRole[x].user.active
			assert response["statuscode"]==200
			assert response["message"]=="Users listed successfully."
     
	#Test case for list users with invalid company_id.
	@pytest.mark.parametrize("company_id",[(30),(40),(50),(60),(15),(70)])
	def test_list_users_with_invalid_company_id(self,client,company_id):
		request=reverse("organization:list-users")
		data={"company_id":company_id}
		getUsers=Users.objects.get(email="projectadmin@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["data"]==[]
		assert len(response["data"])==0
		assert response["message"]=="Users listed successfully."
    
	#Test case for list users with user whose roles are not assined
	@pytest.mark.parametrize("email",[("testuser1@momenttext.com"),("testuser2@momenttext.com")
							,("testuser3@momenttext.com")])
	def test_list_users_without_user_role(self,client,email,setup_user_for_new_password):
		request=reverse("organization:list-users")
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email=email).token}
		data={"company_id":4}
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["message"]=="You are not authorized to list users."
		assert response["statuscode"]== 400
                                   		
	# def test_list_users(self):
	# 	request=reverse("organization:list-users")
	# 	headers={"HTTP_AUTHORIZATION":""}

@pytest.mark.usefixtures("setup_user_for_new_password")						
class Test_create_usercompanyrole():
    
    #Test case for create usercompanyrole with all valid data.
	@pytest.mark.parametrize("flag",[("COMPANY-MANAGEMENT","PROJECT-MANAGEMENT")])
	def test_create_usercompanyrole_with_valid_data(self,client,flag,setup_user_for_new_password):
		request=reverse("organization:create-usercompanyrole")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		getUsers=Users.objects.get(email="testuser1@momenttext.com")
		data={"company":2,"user":getUsers.id,"flag":flag,"role":2}
		getUsersRole=UserCompanyRole.objects.count()
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["data"] == getUsersRole+1
		assert response["isNew"] == True
		assert response["isReplaced"] == False
		assert response["message"] == "UserCompanyRole created successfully."
		assert response["statuscode"] == 200

	#Test case for create usercompanyrole with invalid token.
	def test_create_usercompanyrole_with_invalid_token(self,client,setup_user_for_new_password):
		request=reverse("organization:create-usercompanyrole")
		getUsers=Users.objects.get(email="testuser1@momenttext.com")
		data=json.dumps({"company":2,"user":getUsers.id,"flag":"COMPANY-MANAGEMENT","role":2})
		headers={"HTTP_AUTHORIZATION":fake.uuid4()}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==403
      
	#Test case for create usercompanyrole with missing/invalid parameter.
	def test_create_usercompanyrole_with_invalid_parameter(self,client):
		request=reverse("organization:create-usercompanyrole")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		getUsers=Users.objects.get(email="testuser1@momenttext.com")
		data=json.dumps({"client_id":2,"user":getUsers.id,"flag":"COMPANY-MANAGEMENT","role":2})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
		getUsers=Users.objects.get(email="testuser1@momenttext.com")
		data=json.dumps({"company":2,"user":getUsers.id,"role":2})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
      
	#Test case for create usercompanyrole with invalid user in parameter.
	@pytest.mark.parametrize("user,flag,role",[
		(30,"Project-Management",2),(30,"Project-Management",4),(30,"Company-Management",3)
		,(40,"Company-Management",2),(40,"Project-Management",3),(40,"Project-Management",4)
		,(50,"Project-Management",3),(50,"Company-Management",2),(50,"Company-Management",3)
		,(60,"Company-Management",4),(60,"Project-Management",3),(60,"Company-Management",4)])
	def test_create_usercompanyrole_with_invalid_user(self,client,user,flag,role):
		request=reverse("organization:create-usercompanyrole")
		data=json.dumps({"company":2,"user":user,"flag":flag,"role":role})
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email="su1@momenttext.com").token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="User with the provided ID is not found in the database."
      
	#Test case for create usercompanyrole with invalid role id in parameter.
	@pytest.mark.parametrize("user,flag,role",[
		(3,"Project-Management",21),(3,"Project-Management",14),(3,"Company-Management",31)
		,(4,"Company-Management",12),(4,"Project-Management",33),(4,"Project-Management",44)
		,(5,"Project-Management",23),(5,"Company-Management",24),(5,"Company-Management",33)
		,(2,"Company-Management",6),(6,"Project-Management",36),(6,"Company-Management",46)])
	def test_create_usercompanyrole_with_invalid_role_id(self,client,user,flag,role):
		request=reverse("organization:create-usercompanyrole")
		data=json.dumps({"company":2,"user":user,"flag":flag,"role":role})
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email="su1@momenttext.com").token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Role with the provided ID is not found in the database."
      
	#Test case for create usercompanyrole with invalid company id in parameter.
	@pytest.mark.parametrize("company,user,flag,role",[
		(21,3,"Project-Management",21),(31,3,"Project-Management",14),(41,3,"Company-Management",31)
		,(44,4,"Company-Management",12),(51,4,"Project-Management",33),(13,4,"Project-Management",44)
		,(24,5,"Project-Management",23),(45,5,"Company-Management",24),(54,5,"Company-Management",33)])
	def test_create_usercompanyrole_with_invalid_company_id(self,client,company,user,flag,role):
		request=reverse("organization:create-usercompanyrole")
		data=json.dumps({"company":company,"user":user,"flag":flag,"role":role})
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email="su1@momenttext.com").token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Company with the provided ID is not found in the database."

	#Test case for create usercompanyrole with assigning superuser for company admin 
	@pytest.mark.parametrize("flag",[("COMPANY-MANAGEMENT"),("PROJECT-MANAGEMENT")])
	def test_create_usercompanyrole_with_superuser_as_company_admin(self,client,flag):
		request=reverse("organization:create-usercompanyrole")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		getUsers=Users.objects.get(email="su1@momenttext.com")
		data={"company":2,"user":getUsers.id,"flag":flag,"role":2}
		getUsersRole=UserCompanyRole.objects.count()
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"] == "SUPER-USER cannot be made COMPANY-ADMIN."

	#Test case for create usercompanyrole without user authorization.
	@pytest.mark.parametrize("email,flag",[("testuser@momenttext.com","Company-Management")
                                        ,("user@momenttext.com","Project-Management")])
	def test_create_usercompanyrole_without_authorization(self,client,email,flag):
		request=reverse("organization:create-usercompanyrole")
		data=json.dumps({"company":2,"flag":flag,"role":random.randint(2,4)
			,"user":Users.objects.get(email=email).id})
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email=email).token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="You cannot create the UserCompanyRole."
      
	#Test case for create usercompanyrole with existing user company role
	@pytest.mark.usefixtures("setup_create_usercompanyrole_with_existing_companyrole")
	@pytest.mark.parametrize("flag",[("Company-Management"),("Project-Management")])
	def test_create_usercompanyrole_with_existing_company(self,client,flag):
		request=reverse("organization:create-usercompanyrole")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		users=["testuser{}@momenttext.com".format(x) for x in range(1,6)]
		for user in Users.objects.filter(email__in=users):
			data=json.dumps({"company":5,"user":user.id,"flag":flag,"role":3})
			getUserCompanyRole=UserCompanyRole.objects.get(company_id=5,user=user,role_id=3)
			assert getUserCompanyRole.isActive==False
			response=client.post(request,data=data,content_type="application/json",**headers)
			assert response.status_code==200
			response=response.json()
			assert response["statuscode"]==200
			getUserCompanyRole=UserCompanyRole.objects.get(company_id=5,user=user,role_id=3)
			assert response["data"] == getUserCompanyRole.id
			assert getUserCompanyRole.isActive==True
			assert response["isNew"] == False
			assert response["isReplaced"] == False
			assert response['message'] == 'UserCompanyRole already existed.'
			assert response["statuscode"] == 200
    
	#Test case for create usercompanyrole with user of different companies 
	@pytest.mark.parametrize("client_id",[(3),(4),(5),(6),(1),(7)])
	def test_create_usercompanyrole_with_diff_company(self,client,client_id):
		request=reverse("organization:create-usercompanyrole")
		getUsers=Users.objects.get(email="companyadmin@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		data={"user":3,"company":client_id,"role":3
                  ,"flag":"Company-Management"}
		getCompany=Company.objects.get(id=client_id)
		assert getCompany.state_pin_code is None
		assert getCompany.name is not None
		assert getCompany.city is None
		assert getCompany.address1 is None
		assert getCompany.state is None
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["message"]=="UserCompanyRole created successfully."

	#Test case for create usercompany role with user of a same company with different roles
	@pytest.mark.usefixtures("setup_create_usercompanyrole_with_existing_companyrole")			
	@pytest.mark.parametrize("email,role,company,flag",[
	("testuser1@momenttext.com",3,5,"Company-Management"),("testuser1@momenttext.com",3,5,"Project-Management"),
	("testuser2@momenttext.com",3,5,"Company-Management"),("testuser2@momenttext.com",3,5,"Project-Management"),
	("testuser4@momenttext.com",3,5,"Company-Management"),("testuser4@momenttext.com",3,5,"Project-Management"),
	("testuser5@momenttext.com",3,5,"Company-Management"),("testuser5@momenttext.com",3,5,"Project-Management"),
	                                                 ])
	def test_create_usercompanyrole(self,client,email,role,company,flag):
		request=reverse("organization:create-usercompanyrole")
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email="su1@momenttext.com").token}
		getUsers=Users.objects.get(email=email)
		getCompany=Company.objects.get(id=company)
		data=json.dumps({"user":getUsers.id,"company":getCompany.id,"role":role,"flag":flag})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["isNew"] == False
		assert response["isReplaced"] == False
		assert response["message"]=="UserCompanyRole already existed."

    				
class Test_deactivate_usercompanyrole():

	#Test case for deactivate usercompanyrole with data doesn't exist in db
	@pytest.mark.parametrize("email,role,company",[("testuser1@momenttext.com",2,3)
                            ,("testuser2@momenttext.com",3,3),("testuser3@momenttext.com",4,3)                    
                            ,("testuser4@momenttext.com",2,5),("testuser3@momenttext.com",3,2)                    
                                                ])
	def test_deactivate_usercompanyrole_invalid_usercompanyrole(self,client,email,role,company,setup_saved_user):
		request=reverse("organization:deactivate-usercompanyrole")
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email="su1@momenttext.com").token}
		getUsers=Users.objects.get(email=email)
		data=json.dumps({"user":getUsers.id,"role":role,"company":company})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="UserCompanyRole doesnot exists."

	#Test case for deactivate usercompanyrole with all valid data.
	def test_deactivate_usercompanyrole_with_valid_data(self,client):
		request=reverse("organization:deactivate-usercompanyrole")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		getUsers=Users.objects.get(email="companyadmin@momenttext.com")
		getCompany=Company.objects.get(name="Microsoft")
		data={"company":getCompany.id,"user":getUsers.id,"role":2}
		getUsersRole=UserCompanyRole.objects.get(user=getUsers)
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["data"] == getUsersRole.id
		assert response["message"] == "UserCompanyRole deactivate successfully."
		assert response["statuscode"] == 200
  
    #Test case for deactivate usercompanyrole with all valid data.
	@pytest.mark.parametrize("email,role,company",[("companyadmin@momenttext.com",2,"Microsoft")
                    ,("testuser@momenttext.com",4,"Microsoft"),("user@momenttext.com",4,"Microsoft")                               
                                                   ])
	def test_deactivate_usercompanyrole_with_all_usercompanyrole(self,client,email,role,company):
		request=reverse("organization:deactivate-usercompanyrole")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		getUsers=Users.objects.get(email=email)
		getCompany=Company.objects.get(name=company)
		data={"company":getCompany.id,"user":getUsers.id,"role":role}
		getUsersRole=UserCompanyRole.objects.get(user=getUsers)
		response=client.post(request,data=json.dumps(data),content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==200
		assert response["data"] == getUsersRole.id
		assert response["message"] == "UserCompanyRole deactivate successfully."
		assert response["statuscode"] == 200

	#Test case for deactivate usercompanyrole with invalid token.
	def test_deactivate_usercompanyrole_with_invalid_token(self,client):
		request=reverse("organization:deactivate-usercompanyrole")
		getUsers=Users.objects.get(email="user@momenttext.com")
		data=json.dumps({"company":2,"user":getUsers.id,"role":2})
		headers={"HTTP_AUTHORIZATION":fake.uuid4()}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==403
      
	#Test case for deactivate usercompanyrole with missing/invalid parameter.
	def test_deactivate_usercompanyrole_with_invalid_parameter(self,client):
		request=reverse("organization:deactivate-usercompanyrole")
		getUsers=Users.objects.get(email="su1@momenttext.com")
		headers={"HTTP_AUTHORIZATION":getUsers.token}
		getUsers=Users.objects.get(email="testuser@momenttext.com")
		data=json.dumps({"client_id":2,"user":getUsers.id,"role":2})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
		getUsers=Users.objects.get(email="testuser@momenttext.com")
		data=json.dumps({"company":2,"user":getUsers.id})
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==500
      
	#Test case for deactivate usercompanyrole with invalid user in parameter.
	@pytest.mark.parametrize("user,flag,role",[
		(30,"Project-Management",2),(30,"Project-Management",4),(30,"Company-Management",3)
		,(40,"Company-Management",2),(40,"Project-Management",3),(40,"Project-Management",4)
		,(50,"Project-Management",3),(50,"Company-Management",2),(50,"Company-Management",3)
		,(60,"Company-Management",4),(60,"Project-Management",3),(60,"Company-Management",4)])
	def test_deactivate_usercompanyrole_with_invalid_user(self,client,user,flag,role):
		request=reverse("organization:deactivate-usercompanyrole")
		data=json.dumps({"company":2,"user":user,"flag":flag,"role":role})
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email="su1@momenttext.com").token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="User with the provided ID is not found in the database."
      
	#Test case for deactivate usercompanyrole with invalid role id in parameter.
	@pytest.mark.parametrize("user,flag,role",[
		(3,"Project-Management",21),(3,"Project-Management",14),(3,"Company-Management",31)
		,(4,"Company-Management",12),(4,"Project-Management",33),(4,"Project-Management",44)
		,(5,"Project-Management",23),(5,"Company-Management",24),(5,"Company-Management",33)
		,(2,"Company-Management",6)])
	def test_deactivate_usercompanyrole_with_invalid_role_id(self,client,user,flag,role):
		request=reverse("organization:deactivate-usercompanyrole")
		data=json.dumps({"company":2,"user":user,"flag":flag,"role":role})
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email="su1@momenttext.com").token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Role with the provided ID is not found in the database."
      
	#Test case for deactivate usercompanyrole with invalid company id in parameter.
	@pytest.mark.parametrize("company,user,flag,role",[
		(21,3,"Project-Management",21),(31,3,"Project-Management",14),(41,3,"Company-Management",31)
		,(44,4,"Company-Management",12),(51,4,"Project-Management",33),(13,4,"Project-Management",44)
		,(24,5,"Project-Management",23),(45,5,"Company-Management",24),(54,5,"Company-Management",33)])
	def test_deactivate_usercompanyrole_with_invalid_company_id(self,client,company,user,flag,role):
		request=reverse("organization:deactivate-usercompanyrole")
		data=json.dumps({"company":company,"user":user,"flag":flag,"role":role})
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email="su1@momenttext.com").token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="Company with the provided ID is not found in the database."
  
	#Test case for deactivate usercompanyrole without user authorization.
	@pytest.mark.parametrize("email",[("testuser@momenttext.com")
                                        ,("user@momenttext.com")])
	def test_deactivate_usercompanyrole_without_authorization(self,client,email):
		request=reverse("organization:deactivate-usercompanyrole")
		data=json.dumps({"company":2,"role":random.randint(2,4)
			,"user":Users.objects.get(email=email).id})
		headers={"HTTP_AUTHORIZATION":Users.objects.get(email=email).token}
		response=client.post(request,data=data,content_type="application/json",**headers)
		assert response.status_code==200
		response=response.json()
		assert response["statuscode"]==400
		assert response["message"]=="You cannot create the UserCompanyRole."
      	
   