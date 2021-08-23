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
        
        
        
        
        