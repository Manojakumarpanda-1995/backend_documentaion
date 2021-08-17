import pytest
from django.urls import resolve,reverse

class Test_urls:
    # (func=usermanagement.views.login, args=(), kwargs={}, url_name=loginapi, 
    #  app_names=['usermanagement'], namespaces=['usermanagement'], route=access/loginapi)
    def test_login_url(self,*args, **kwargs):
        request=reverse("usermanagement:loginapi")
        response=resolve(request)
        assert "usermanagement" in response.app_name
        assert response.route=="access/loginapi"
        assert response.view_name=="usermanagement:loginapi"
        assert response.url_name=="loginapi"
        
    def test_reset_password_url(self,*args, **kwargs):
        request=reverse("usermanagement:reset-password")
        response=resolve(request)
        assert "usermanagement" in response.app_name
        assert response.route=="access/reset-password"
        assert response.view_name=="usermanagement:reset-password"
        assert response.url_name=="reset-password"
        
    def test_update_password_url(self,*args, **kwargs):
        request=reverse("usermanagement:update-password")
        response=resolve(request)
        assert "usermanagement" in response.app_name
        assert response.route=="access/update-password"
        assert response.view_name=="usermanagement:update-password"
        assert response.url_name=="update-password"
        
    def test_new_password_url(self,*args, **kwargs):
        request=reverse("usermanagement:new-password")
        response=resolve(request)
        assert "usermanagement" in response.app_name
        assert response.route=="access/new-password"
        assert response.view_name=="usermanagement:new-password"
        assert response.url_name=="new-password"
        
    def test_logout_url(self,*args, **kwargs):
        request=reverse("usermanagement:logout")
        response=resolve(request)
        assert "usermanagement" in response.app_name
        assert response.route=="access/logout"
        assert response.view_name=="usermanagement:logout"
        assert response.url_name=="logout"
        
    def test_check_token_url(self,*args, **kwargs):
        request=reverse("usermanagement:check-token")
        response=resolve(request)
        assert "usermanagement" in response.app_name
        assert response.route=="access/check-token"
        assert response.view_name=="usermanagement:check-token"
        assert response.url_name=="check-token"
        
    def test_download_file_url(self,*args, **kwargs):
        request=reverse("usermanagement:download-file")
        response=resolve(request)
        assert "usermanagement" in response.app_name
        assert response.route=="access/download-file"
        assert response.view_name=="usermanagement:download-file"
        assert response.url_name=="download-file"
        
    def test_create_role_url(self,*args, **kwargs):
        request=reverse("usermanagement:create-role")
        response=resolve(request)
        assert "usermanagement" in response.app_name
        assert response.route=="access/create-role"
        assert response.view_name=="usermanagement:create-role"
        assert response.url_name=="create-role"
        
    def test_get_role_url(self,*args, **kwargs):
        request=reverse("usermanagement:get-role")
        response=resolve(request)
        assert "usermanagement" in response.app_name
        assert response.route=="access/get-role"
        assert response.view_name=="usermanagement:get-role"
        assert response.url_name=="get-role"
        
    def test_register_user_url(self,*args, **kwargs):
        request=reverse("usermanagement:register-user")
        response=resolve(request)
        assert "usermanagement" in response.app_name
        assert response.route=="access/register-user"
        assert response.view_name=="usermanagement:register-user"
        assert response.url_name=="register-user"
        
    def test_register_worker_url(self,*args, **kwargs):
        request=reverse("usermanagement:register-worker")
        response=resolve(request)
        assert "usermanagement" in response.app_name
        assert response.route=="access/register-worker"
        assert response.view_name=="usermanagement:register-worker"
        assert response.url_name=="register-worker"
        
    def test_register_access_url(self,*args, **kwargs):
        request=reverse("usermanagement:register-access-request")
        response=resolve(request)
        assert "usermanagement" in response.app_name
        assert response.route=="access/register-access-request"
        assert response.view_name=="usermanagement:register-access-request"
        assert response.url_name=="register-access-request"
        
    def test_edit_user_url(self,*args, **kwargs):
        request=reverse("usermanagement:edit-user")
        response=resolve(request)
        assert "usermanagement" in response.app_name
        assert response.route=="access/edit-user"
        assert response.view_name=="usermanagement:edit-user"
        assert response.url_name=="edit-user"
        
    def test_edit_user_byid_url(self,*args, **kwargs):
        request=reverse("usermanagement:edit-user-byid")
        response=resolve(request)
        assert "usermanagement" in response.app_name
        assert response.route=="access/edit-user-byid"
        assert response.view_name=="usermanagement:edit-user-byid"
        assert response.url_name=="edit-user-byid"
        
    def test_deactivate_user_url(self,*args, **kwargs):
        request=reverse("usermanagement:deactivate-user")
        response=resolve(request)
        assert "usermanagement" in response.app_name
        assert response.route=="access/deactivate-user"
        assert response.view_name=="usermanagement:deactivate-user"
        assert response.url_name=="deactivate-user"
        
    def test_list_user_byemail_url(self,*args, **kwargs):
        request=reverse("usermanagement:list-user-byemail")
        response=resolve(request)
        assert "usermanagement" in response.app_name
        assert response.route=="access/list-user-byemail"
        assert response.view_name=="usermanagement:list-user-byemail"
        assert response.url_name=="list-user-byemail"
        
    # def test_logout_url(self,*args, **kwargs):
    #     request=reverse("usermanagement:logout")
    #     response=resolve(request)
    #     assert "usermanagement" in response.app_name
    #     assert response.route=="access/logout"
    #     assert response.view_name=="usermanagement:logout"
    #     assert response.url_name=="logout"
        