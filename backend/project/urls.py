from django.urls import path
from . import views
    

urlpatterns = [
    path('create-project', views.create_project.as_view()),
    path('assign-project', views.assign_project.as_view()),
    path('list-project', views.list_project.as_view()),
    path('list-project-byemail', views.list_projects_byemail.as_view()),
    path('edit-project', views.edit_project.as_view()),
    path('delete-project', views.delete_project.as_view()),
    path('edit-project-user-id', views.edit_project_user_id.as_view()),
    path('create-project-user', views.create_project_user.as_view()),	
    path('list-users-by-project', views.list_users_by_project.as_view()),
    path('list-projects-for-users', views.list_project_for_users.as_view()),
## File Upload
    path('bulk-user-upload', views.bulk_upload_users.as_view()),
## File Download
    path('bulk-user-download', views.bulk_download_users.as_view()),
    path('download-file', views.download_file.as_view()),
    path('download-large-file', views.download_large_file.as_view()),
## Get Progress
    path('get-progress', views.get_progress.as_view()),
# Logs	
    path('generate-user-logs', views.generate_user_logs.as_view()),
]