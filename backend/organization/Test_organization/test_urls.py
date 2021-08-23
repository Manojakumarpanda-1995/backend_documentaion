import pytest
from django.urls import resolve,reverse
from organization import views

class Test_urls:
	# (func=organization.views.login, args=(), kwargs={}, url_name=create-company, 
	#  app_names=['organization'], namespaces=['organization'], route=org/create-company)
	def test_create_company(self,*args, **kwargs):
		request=reverse("organization:create-company")
		response=resolve(request)
		assert "organization" in response.app_name
		assert response.route=="org/create-company"
		assert response.view_name=="organization:create-company"
		assert response.url_name=="create-company"
		assert response.func.view_class==views.create_company
		
	def test_get_company_url(self,*args, **kwargs):
		request=reverse("organization:get-company")
		response=resolve(request)
		assert "organization" in response.app_name
		assert response.route=="org/get-company"
		assert response.view_name=="organization:get-company"
		assert response.url_name=="get-company"
		assert response.func.view_class==views.get_company
		
	def test_create_usercompanyrole_url(self,*args, **kwargs):
		request=reverse("organization:create-usercompanyrole")
		response=resolve(request)
		assert "organization" in response.app_name
		assert response.route=="org/create-usercompanyrole"
		assert response.view_name=="organization:create-usercompanyrole"
		assert response.url_name=="create-usercompanyrole"
		assert response.func.view_class==views.create_usercompanyrole
		
	def test_deactivate_usercompanyrole_url(self,*args, **kwargs):
		request=reverse("organization:deactivate-usercompanyrole")
		response=resolve(request)
		assert "organization" in response.app_name
		assert response.route=="org/deactivate-usercompanyrole"
		assert response.view_name=="organization:deactivate-usercompanyrole"
		assert response.url_name=="deactivate-usercompanyrole"
		assert response.func.view_class==views.deactivate_usercompanyrole
	
	def test_delete_company_url(self,*args, **kwargs):
		request=reverse("organization:delete-company")
		response=resolve(request)
		assert "organization" in response.app_name
		assert response.route=="org/delete-company"
		assert response.view_name=="organization:delete-company"
		assert response.url_name=="delete-company"
		assert response.func.view_class==views.delete_company
		
	def test_list_company_url(self,*args, **kwargs):
		request=reverse("organization:list-company")
		response=resolve(request)
		assert "organization" in response.app_name
		assert response.route=="org/list-company"
		assert response.view_name=="organization:list-company"
		assert response.url_name=="list-company"
		assert response.func.view_class==views.list_company
		
	def test_list_company_byemail_url(self,*args, **kwargs):
		request=reverse("organization:list-company-byemail")
		response=resolve(request)
		assert "organization" in response.app_name
		assert response.route=="org/list-company-byemail"
		assert response.view_name=="organization:list-company-byemail"
		assert response.url_name=="list-company-byemail"
		assert response.func.view_class==views.list_company_byemail
		
	def test_edit_company_url(self,*args, **kwargs):
		request=reverse("organization:edit-company")
		response=resolve(request)
		assert "organization" in response.app_name
		assert response.route=="org/edit-company"
		assert response.view_name=="organization:edit-company"
		assert response.url_name=="edit-company"
		assert response.func.view_class==views.edit_company
		
	def test_get_company_info_url(self,*args, **kwargs):
		request=reverse("organization:get-company-info")
		response=resolve(request)
		assert "organization" in response.app_name
		assert response.route=="org/get-company-info"
		assert response.view_name=="organization:get-company-info"
		assert response.url_name=="get-company-info"
		assert response.func.view_class==views.get_company_info
		
	def test_edit_company_info_url(self,*args, **kwargs):
		request=reverse("organization:edit-company-info")
		response=resolve(request)
		assert "organization" in response.app_name
		assert response.route=="org/edit-company-info"
		assert response.view_name=="organization:edit-company-info"
		assert response.url_name=="edit-company-info"
		assert response.func.view_class==views.edit_company_info
		
	def test_list_users_url(self,*args, **kwargs):
		request=reverse("organization:list-users")
		response=resolve(request)
		assert "organization" in response.app_name
		assert response.route=="org/list-users"
		assert response.view_name=="organization:list-users"
		assert response.url_name=="list-users"
		assert response.func.view_class==views.list_users
		
   
   