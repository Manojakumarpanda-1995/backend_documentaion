from django.urls import path
from . import views

app_name="usermanagement"

urlpatterns = [
    ## Login	
    path('', views.login.as_view(),name="loginapi"),
    path('loginapi', views.login.as_view(),name="loginapi"),
    # #Forgot password #Works only with email integration
    path('reset-password', views.reset_password_request.as_view(),name="reset-password"),
    # THis API is used at forgot password stage
    path('update-password', views.update_password.as_view(),name="update-password"),
    path('new-password', views.set_new_password.as_view(),name="new-password"),
    path('logout', views.logout.as_view(),name="logout"),
    # #Validate token	
    path('check-token', views.check_token.as_view(),name="check-token"),	
    # # Email verification
    path('validate-emailid', views.validate_emailid.as_view(),name="validate-emailid"), #GET REQUEST
    # File upload / download	
    # path('upload-file', views.upload_file.as_view(),name="upload-file"),
    path('download-file', views.download_file.as_view(),name="download-file"),
    ## Get activity logs	
    # path('list-activity-logs', views.list_activity_logs.as_view(),name="list-activity-logs"),
    ## Roles   
    path('create-role', views.create_role.as_view(),name="create-role"),
    path('get-role', views.get_role.as_view(),name="get-role"),
    ## User
    path('register-user', views.register_user.as_view(),name="register-user"),
    path('register-worker', views.register_worker.as_view(),name="register-worker"),
    path('register-access-request', views.register_access_request.as_view(),name="register-access-request"),
    path('edit-user', views.edit_user.as_view(),name="edit-user"),
    path('edit-user-byid', views.edit_user_byid.as_view(),name="edit-user-byid"),
    path('deactivate-user', views.deactivate_user.as_view(),name="deactivate-user"),
    path('list-user-byemail', views.list_user_byemail.as_view(),name="list-user-byemail"),
]