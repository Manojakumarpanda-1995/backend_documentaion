from django.urls import path
from . import views

app_name="project"    

urlpatterns = [
    path('create-project', views.create_project.as_view(),name="create-project"),
    path('assign-project', views.assign_project.as_view(),name="assign-project"),
    path('list-project', views.list_project.as_view(),name="list-project"),
    path('list-project-byemail', views.list_projects_byemail.as_view(),name="list-project-byemail"),
    path('edit-project', views.edit_project.as_view(),name="edit-project"),
    path('delete-project', views.delete_project.as_view(),name="delete-project"),
    path('edit-project-user-id', views.edit_project_user_id.as_view(),name="edit-project-user-id"),
    path('create-project-user', views.create_project_user.as_view(),name="create-project-user"),	
    path('list-users-by-project', views.list_users_by_project.as_view(),name="list-users-by-project"),
    path('list-projects-for-users', views.list_project_for_users.as_view(),name="list-projects-for-users"),
## File Upload
    path('bulk-user-upload', views.bulk_upload_users.as_view(),name="bulk-user-upload"),
## File Download
    path('bulk-user-download', views.bulk_download_users.as_view(),name="bulk-user-download"),
    path('download-file', views.download_file.as_view(),name="download-file"),
    path('download-large-file', views.download_large_file.as_view(),name="download-large-file"),
## Get Progress
    path('get-progress', views.get_progress.as_view(),name="get-progress"),
# Logs	
    path('generate-user-logs', views.generate_user_logs.as_view(),name="generate-user-logs"),
]