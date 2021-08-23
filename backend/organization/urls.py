from django.urls import path
from . import views

app_name="organization"    

urlpatterns = [
    # path('list-activity-logs', views.list_activity_logs.as_view()),
    ## Roles
    # path('create-role', views.create_role.as_view()),
    # path('list-roles', views.list_roles.as_view()),
    # path('delete-role', views.delete_role.as_view()), # Cannot delete role if users are associated with a role
    # path('dashboard-count', views.dashboard_count.as_view()),
    ## Company
    ## only superuser can create the company
    path('create-company', views.create_company.as_view(),name="create-company"), #ok
    path('get-company', views.get_company.as_view(),name="get-company"),#ok
    path('create-usercompanyrole', views.create_usercompanyrole.as_view(),name="create-usercompanyrole"),#ok
    path('deactivate-usercompanyrole', views.deactivate_usercompanyrole.as_view(),name="deactivate-usercompanyrole"),#ok
    # path('assign-company-admin', views.assign_company_admin.as_view()),
    # path('edit-company-admin', views.edit_company_admin.as_view()),
    
    path('delete-company', views.delete_company.as_view(),name="delete-company"),#ok
    # path('company-status', views.company_status.as_view()), #activate-deactivate
    path('list-company', views.list_company.as_view(),name="list-company"),#ok
    path('list-company-byemail', views.list_company_byemail.as_view(),name="list-company-byemail"),#ok
    path('edit-company', views.edit_company.as_view(),name="edit-company"),#ok
    path('get-company-info', views.get_company_info.as_view(),name="get-company-info"),#ok
    path('edit-company-info', views.edit_company_info.as_view(),name="edit-company-info"),#ok
    # path('fetch-company-details', views.fetch_company_details.as_view()),
    # path('company-details', views.company_details.as_view()), ################ make
    ## Projects
    # path('create-project', views.create_project.as_view()), ################ make
    # path('assign-project-admin', views.assign_project_admin.as_view()),
    # path('delete-project', views.delete_project.as_view()),
    # path('project-status', views.project_status.as_view()),
    # path('list-projects', views.list_projects.as_view()), #If no input parameter provided, will list all projects for super user & company level projects for company admin
    # path('dropdown-projects', views.dropdown_projects.as_view()), 
    # path('edit-project', views.edit_project.as_view()),
    # # path('assign-company', views.assign_company.as_view()),#Assign project to company
    ## User management	
    # path('check-user', views.check_user.as_view()), # checks if the user exists 
    # path('create-user', views.create_user.as_view()), # App level
    # path('user-companies',views.user_companies.as_view()),
    # path('user-projects',views.user_projects.as_view()),
    # # path('reset-user-password', views.reset_user_password.as_view()), # App level 
    # path('delete-user', views.delete_user.as_view()), # App level
    # # path('user-status', views.user_status.as_view()),  # It will have a mandatory parameter - project id
    path('list-users', views.list_users.as_view(),name="list-users"),#ok # IT has 2 input parameters, company & project. If no input parameter provided, then this will list down all users for superuser, all company users for a company admin, all project users for a project admin.
    # path('edit-user', views.edit_user.as_view()), # App level
    # path('assign-role-project', views.assign_role_project.as_view()),	# Project level 
]