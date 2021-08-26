from django.urls import reverse,resolve
from project import views

class Test_urls():
	
	def test_create_project_url(self,*args,**kwargs):
		request=reverse("project:create-project")
		response=resolve(request)
		assert "project" in response.app_name
		assert "project" in response.namespace
		assert response.args==()
		assert response.kwargs=={}
		assert response.func.view_class==views.create_project
		assert response.route=="project/create-project"
		assert response.url_name=="create-project"
		assert response.view_name=="project:create-project"
  
	def test_assign_project_url(self,*args, **kwargs):
		request=reverse("project:assign-project")
		response=resolve(request)
		assert "project" in response.namespace
		assert "project" in response.app_name
		assert response.args==()
		assert response.kwargs=={} 
		assert response.func.view_class==views.assign_project
		assert response.route=="project/assign-project"
		assert response.url_name=="assign-project"
		assert response.view_name=="project:assign-project"
		
	def test_list_project_url(self,*args, **kwargs):
		request=reverse("project:list-project")
		response=resolve(request)
		assert "project" in response.namespace
		assert "project" in response.app_name
		assert response.args==()
		assert response.kwargs=={} 
		assert response.func.view_class==views.list_project
		assert response.route=="project/list-project"
		assert response.url_name=="list-project"
		assert response.view_name=="project:list-project"
		
	def test_list_projects_byemail_url(self,*args, **kwargs):
		request=reverse("project:list-project-byemail")
		response=resolve(request)
		assert "project" in response.namespace
		assert "project" in response.app_name
		assert response.args==()
		assert response.kwargs=={} 
		assert response.func.view_class==views.list_projects_byemail
		assert response.route=="project/list-project-byemail"
		assert response.url_name=="list-project-byemail"
		assert response.view_name=="project:list-project-byemail"
		
	def test_edit_project_url(self,*args, **kwargs):
		request=reverse("project:edit-project")
		response=resolve(request)
		assert response.func.view_class==views.edit_project
		assert "project" in response.namespace
		assert "project" in response.app_name
		assert response.args==()
		assert response.kwargs=={} 
		assert response.route=="project/edit-project"
		assert response.url_name=="edit-project"
		assert response.view_name=="project:edit-project"
		
	def test_delete_project_url(self,*args, **kwargs):
		request=reverse("project:delete-project")
		response=resolve(request)
		assert response.func.view_class==views.delete_project
		assert "project" in response.namespace
		assert "project" in response.app_name
		assert response.args==()
		assert response.kwargs=={}
		assert response.route=="project/delete-project"
		assert response.url_name=="delete-project"
		assert response.view_name=="project:delete-project"
		 
	def test_edit_project_user_id_url(self,*args, **kwargs):
		request=reverse("project:edit-project-user-id")
		response=resolve(request)
		assert response.func.view_class==views.edit_project_user_id
		assert "project" in response.namespace
		assert "project" in response.app_name
		assert response.args==()
		assert response.kwargs=={} 
		assert response.route=="project/edit-project-user-id"
		assert response.url_name=="edit-project-user-id"
		assert response.view_name=="project:edit-project-user-id"
		
	def test_create_project_user_url(self,*args, **kwargs):
		request=reverse("project:create-project-user")
		response=resolve(request)
		assert "project" in response.namespace
		assert "project" in response.app_name
		assert response.args==()
		assert response.kwargs=={} 
		assert response.func.view_class==views.create_project_user
		assert response.route=="project/create-project-user"
		assert response.url_name=="create-project-user"
		assert response.view_name=="project:create-project-user"
			
	def test_list_users_by_project_url(self,*args, **kwargs):
		request=reverse("project:list-users-by-project")
		response=resolve(request)
		assert "project" in response.namespace
		assert "project" in response.app_name
		assert response.args==()
		assert response.kwargs=={} 
		assert response.func.view_class==views.list_users_by_project
		assert response.route=="project/list-users-by-project"
		assert response.url_name=="list-users-by-project"
		assert response.view_name=="project:list-users-by-project"
		
	def test_list_projects_for_users_url(self,*args, **kwargs):
		request=reverse("project:list-projects-for-users")
		response=resolve(request)
		assert "project" in response.namespace
		assert "project" in response.app_name
		assert response.args==()
		assert response.kwargs=={} 
		assert response.func.view_class==views.list_project_for_users
		assert response.route=="project/list-projects-for-users"
		assert response.url_name=="list-projects-for-users"
		assert response.view_name=="project:list-projects-for-users"
		
	# ## File Upload
	def test_bulk_user_upload_url(self,*args, **kwargs):
		request=reverse("project:bulk-user-upload")
		response=resolve(request)
		assert "project" in response.namespace
		assert "project" in response.app_name
		assert response.args==()
		assert response.kwargs=={}
		assert response.func.view_class==views.bulk_upload_users
		assert response.route=="project/bulk-user-upload"
		assert response.url_name=="bulk-user-upload"
		assert response.view_name=="project:bulk-user-upload"
		 
	# ## File Download
	def test_bulk_user_download_url(self,*args, **kwargs):
		request=reverse("project:bulk-user-download")
		response=resolve(request)
		assert "project" in response.namespace
		assert "project" in response.app_name
		assert response.args==()
		assert response.kwargs=={} 
		assert response.func.view_class==views.bulk_download_users
		assert response.route=="project/bulk-user-download"
		assert response.url_name=="bulk-user-download"
		assert response.view_name=="project:bulk-user-download"
		
	def test_download_url(self,*args, **kwargs):
		request=reverse("project:download-file")
		response=resolve(request)
		assert "project" in response.namespace
		assert "project" in response.app_name
		assert response.args==()
		assert response.kwargs=={} 
		assert response.func.view_class==views.download_file
		assert response.route=="project/download-file"
		assert response.url_name=="download-file"
		assert response.view_name=="project:download-file"
		
	def test_download_large_file_url(self,*args, **kwargs):
		request=reverse("project:download-large-file")
		response=resolve(request)
		assert "project" in response.namespace
		assert "project" in response.app_name
		assert response.args==()
		assert response.kwargs=={} 
		assert response.func.view_class==views.download_large_file
		assert response.route=="project/download-large-file"
		assert response.url_name=="download-large-file"
		assert response.view_name=="project:download-large-file"
		
	# ## Get Progress
	def test_get_progress_url(self,*args, **kwargs):
		request=reverse("project:get-progress")
		response=resolve(request)
		assert "project" in response.namespace
		assert "project" in response.app_name
		assert response.args==()
		assert response.kwargs=={} 
		assert response.func.view_class==views.get_progress
		assert response.route=="project/get-progress"
		assert response.url_name=="get-progress"
		assert response.view_name=="project:get-progress"
		
	# # Logs	
	def test_generate_user_logs_url(self,*args, **kwargs):
		request=reverse("project:generate-user-logs")
		response=resolve(request)
		assert "project" in response.namespace
		assert "project" in response.app_name
		assert response.args==()
		assert response.kwargs=={}
		assert response.func.view_class==views.generate_user_logs
		assert response.route=="project/generate-user-logs"
		assert response.url_name=="generate-user-logs"
		assert response.view_name=="project:generate-user-logs"
	
 
	