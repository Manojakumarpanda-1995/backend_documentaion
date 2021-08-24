from datetime import datetime, timedelta
from _pytest.compat import get_default_arg_names

import faker
import pytest
from organization.models import *
from usermanagement.models import *


class Test_Company():
	
	def test_company_for_administrator(self):
		getCompany=Company.objects.get(id=1)
		assert getCompany.name=="Administrator"
		assert getCompany.created_by==Users.objects.filter(id=1)[0]
		assert getCompany.updated_by==Users.objects.filter(id=1)[0]
		assert getCompany.active==True
		assert getCompany.city is None
		assert getCompany.address1 is None
		assert getCompany.address2 is None
		assert getCompany.state is None
		assert getCompany.country is None
		assert getCompany.partner_name is None
		assert getCompany.state_pin_code is None
	
	@pytest.mark.parametrize("company,id",[("Google",2)
				,("Gmail",3),("Amazon",4),("Tesla",5),("Infosys",6),("Tata",7)])	
	def test_company(self,company,id):
		assert Company.objects.count()==8	 
		getCompany=Company.objects.get(name=company)
		assert getCompany.name==company
		assert getCompany.id==id
		assert getCompany.created_by==Users.objects.filter(id=1)[0]
		assert getCompany.updated_by==Users.objects.filter(id=1)[0]
		assert getCompany.active==True
		assert getCompany.city is None
		assert getCompany.address1 is None
		assert getCompany.address2 is None
		assert getCompany.state is None
		assert getCompany.country is None
		assert getCompany.partner_name is None
		assert getCompany.state_pin_code is None
	
	@pytest.mark.parametrize("company,status",[("Momenttext",False)
				,("Allen Solly",True),("Mahindra",True),("Peter England",False),("Honda",False)])				  
	def test_random_company(self,company,status,setup_test_company):
		assert len(Company.objects.filter(active=False))==3
		assert len(Company.objects.filter(active=True))==10
		getCompany=Company.objects.get(name=company)
		assert getCompany.name==company
		assert getCompany.created_by==Users.objects.filter(id=1)[0]
		assert getCompany.updated_by==Users.objects.filter(id=1)[0]
		assert getCompany.active==status
		assert getCompany.city is not None
		assert getCompany.address1 is not None
		assert getCompany.address2 is None
		assert getCompany.state is not None
		assert getCompany.country is not None
		assert getCompany.partner_name is not None
		assert getCompany.state_pin_code is not None

class Test_CompanyInfo():
			
	def test_company_info(self):
		# assert Company.objects.count()==CompanyInfo.objects.count()	  
		getCompanies=Company.objects.exclude(name="Microsoft")
		for company in getCompanies:
			getCompanyInfo=CompanyInfo.objects.get(company=company)
			assert getCompanyInfo.logo is not None
			assert getCompanyInfo.corporate_type =="Health Insurance"
			assert getCompanyInfo.number_of_emploies is not None
			assert getCompanyInfo.type=="Health"
			assert getCompanyInfo.links is not None
			assert getCompanyInfo.about is not None
			assert getCompanyInfo.active==True
			assert getCompanyInfo.created_by==Users.objects.get(id=1)
			assert getCompanyInfo.updated_by==Users.objects.get(id=1) 
	
	@pytest.mark.parametrize("name",[("Momenttext")
				,("Allen Solly"),("Mahindra"),("Peter England"),("Honda")])
	def test_all_company_info(self,name,setup_company_info):
     
		companies=setup_company_info	  
		for company in companies:
			getCompanyInfo=CompanyInfo.objects.get(company__name=company["company"])
			assert getCompanyInfo.logo is not None
			assert getCompanyInfo.corporate_type =="Health Insurance"
			assert getCompanyInfo.number_of_emploies is not None
			assert getCompanyInfo.type=="Health"
			assert getCompanyInfo.links is not None
			assert getCompanyInfo.about is not None
			assert getCompanyInfo.active==company["status"]
			assert getCompanyInfo.created_by==Users.objects.get(id=1)
			assert getCompanyInfo.updated_by==Users.objects.get(id=1) 
		
class Test_UserCompanyRole():
    
	def test_usercompany_role_superuser(self):
		assert UserCompanyRole.objects.count()==5
		getUser=Users.objects.get(id=1)
		getUserCompanyRole=UserCompanyRole.objects.get(user=getUser)
		assert getUserCompanyRole.role.role_name=="SUPER-USER"		
		assert getUserCompanyRole.company.id==1		
		assert getUserCompanyRole.company.name=="Administrator"
		assert getUserCompanyRole.created_by==getUser		
		assert getUserCompanyRole.updated_by==getUser		
		assert getUserCompanyRole.isActive==True		
		assert getUserCompanyRole.user.active==True		
  
	@pytest.mark.parametrize("email,company_id,role",[
            ("companyadmin@momenttext.com",8,"COMPANY-ADMIN")
            ,("projectadmin@momenttext.com",8,"PROJECT-ADMIN")
            ,("testuser@momenttext.com",8,"USER")
            ,("user@momenttext.com",8,"USER")
	 			] )
	def test_usercompanyrole(self,email,company_id,role):
		assert UserCompanyRole.objects.count()==5
		getUser=Users.objects.get(email=email)
		getCompany=Company.objects.get(id=company_id)
		getUserCompanyRole=UserCompanyRole.objects.get(user=getUser)
		assert getUserCompanyRole.role.role_name==role		
		assert getUserCompanyRole.company.id==company_id	
		assert getUserCompanyRole.company.name==getCompany.name
		assert getUserCompanyRole.created_by_id==1		
		assert getUserCompanyRole.updated_by_id==1		
		assert getUserCompanyRole.isActive==True		
		assert getUserCompanyRole.user.active==True		
  
	@pytest.mark.parametrize("user,id,role",[
						 ("testuser1@momenttext.com",2,"company-admin")
						,("testuser1@momenttext.com",3,"company-admin")
						,("testuser2@momenttext.com",2,"project-admin")
						,("testuser2@momenttext.com",3,"project-admin")
						,("testuser3@momenttext.com",1,"project-admin")
						,("testuser3@momenttext.com",3,"user")
						,("testuser4@momenttext.com",4,"company-admin")
						,("testuser5@momenttext.com",4,"user")
						,("testuser6@momenttext.com",1,"user")
						,("testuser6@momenttext.com",2,"user")
						,("testuser6@momenttext.com",3,"user")
						,("testuser6@momenttext.com",4,"user")
      					])
	def test_all_usercompanyrole(self,user,id,role,setup_usercompany_role):

		company=setup_usercompany_role
		getUserCompanyRole=UserCompanyRole.objects.get(user__email=user
                                                 	,company__name=company[id-1]
                                                  	,role__role_name=role.upper())
		assert getUserCompanyRole.company.name==company[id-1]
		assert getUserCompanyRole.role.role_name==role.upper()
		assert getUserCompanyRole.user.active==Users.objects.get(email=user).active