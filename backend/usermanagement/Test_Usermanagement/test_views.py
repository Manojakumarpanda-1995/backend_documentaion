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


class Test_login():
    
    def test_login_with_valid_data(self,client):
        
        request=reverse("usermanagement:loginapi")
        data={"email":"su1@kpmg.com","password":"Password@123"}
        response=client.post(request,data=json.dumps(data)
                             ,content_type="application/json")
        assert response.status_code==200
        data = response.json()
        assert data["statuscode"]==200
        assert data["token"]==Users.objects.get(id=1).token
        assert data["name"]=="backend Super User 1"
        assert data["email"]=="su1@kpmg.com"
        assert data["company_id"]== 1
        assert data["role"]=="SUPER-USER"
        
    def test_login_with_invalid_data(self,client):
        
        request=reverse("usermanagement:loginapi")
        data={"email":"su1@kpmg.com","password":"Password@12343"}
        response=client.post(request,data=json.dumps(data)
                             ,content_type="application/json")
        assert response.status_code==200
        data = response.json()
        assert data["statuscode"]==400
        assert data["message"]=="The username or password is not correct."
        user=Users.objects.get(email=data['email'])
        curr_access=AccessManagement.objects.get(name=user)
        assert curr_access.password_attempts == 1
        
    def test_login_with_invalid_data(self,client):
        
        request=reverse("usermanagement:loginapi")
        data={"email":"su1@gmail.com","password":"Password@123"}
        response=client.post(request,data=json.dumps(data)
                             ,content_type="application/json")
        assert response.status_code==200
        data = response.json()
        assert data["statuscode"]==400
        assert data["message"]=="Invalid Email."



