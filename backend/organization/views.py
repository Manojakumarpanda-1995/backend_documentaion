from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView

##Importing mixins
from organization.mixins.create_company_mixin import Create_Company_Schema
from organization.mixins.create_usercompany_role_mixin import \
    Create_Usercompany_Role_Schema
from organization.mixins.deactivate_usercompany_role_mixin import \
    Deactivate_Usercompany_Role_Schema
from organization.mixins.delete_company_mixin import Delete_Company_Schema
from organization.mixins.edit_company_mixin import Edit_Company_Schema
from organization.mixins.edit_company_info_mixin import Edit_Company_Info_Schema
from organization.mixins.get_company_mixin import Get_Company_Schema
from organization.mixins.get_company_info_mixin import Get_Company_Info_Schema
from organization.mixins.list_company_mixin import List_Company_Schema
from organization.mixins.list_company_byemail_mixin import \
    List_Company_Byemail_Schema
from organization.mixins.list_users_mixin import List_Users_Schema
## Roles
from organization.utils.create_company import func_create_company
from organization.utils.create_usercompanyrole import \
    func_create_usercompanyrole
from organization.utils.deactivate_usercompanyrole import \
    func_deactivate_usercompanyrole
from organization.utils.delete_company import func_delete_company
from organization.utils.edit_company import func_edit_company
from organization.utils.get_company import func_get_company
from organization.utils.edit_company_info import func_edit_company_info
from organization.utils.get_company_info import func_get_company_info
from organization.utils.list_company import func_list_company
from organization.utils.list_company_byemail import func_list_company_byemail
from organization.utils.list_users import func_list_users

# Create your views here.

### Company ##########
class list_company(APIView,List_Company_Schema):
	permission_classes=(AllowAny,)
	allowed_methods=("POST",)
	schema=AutoSchema(manual_fields=List_Company_Schema().get_manual_fields())
    
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			 "Requested_URL": request.META["PATH_INFO"],
			 
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_list_company(request_data,token)
		return Response(response)

class list_company_byemail(APIView,List_Company_Byemail_Schema):
	permission_classes=(AllowAny,)
	allowed_methods=("POST",)
	schema=AutoSchema(manual_fields=List_Company_Byemail_Schema().get_manual_fields())
 
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			 "Requested_URL": request.META["PATH_INFO"],
			 
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_list_company_byemail(request_data,token)
		return Response(response)

class create_company(APIView,Create_Company_Schema):
	permission_classes=(AllowAny,)
	allowed_methods=("POST",)
	schema=AutoSchema(manual_fields=Create_Company_Schema().get_manual_fields())
	
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			 "Requested_URL": request.META["PATH_INFO"],
			 
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_create_company(request_data,token)
		return Response(response)

class get_company(APIView,Get_Company_Schema):
	permission_classes=(AllowAny,)
	allowed_methods=("POST",)
	schema=AutoSchema(manual_fields=Get_Company_Schema().get_manual_fields())
 
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			 "Requested_URL": request.META["PATH_INFO"],
			 
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_get_company(request_data,token)
		return Response(response)

class edit_company(APIView,Edit_Company_Schema):
	permission_classes=(AllowAny,)
	allowed_methods=("POST",)
	schema=AutoSchema(manual_fields=Edit_Company_Schema().get_manual_fields())
 
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			 "Requested_URL": request.META["PATH_INFO"],
			 
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_edit_company(request_data,token)
		return Response(response)

class get_company_info(APIView,Get_Company_Info_Schema):
	permission_classes=(AllowAny,)
	allowed_methods=("POST",)
	schema=AutoSchema(manual_fields=Get_Company_Info_Schema().get_manual_fields())
 
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			 "Requested_URL": request.META["PATH_INFO"],
			 
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_get_company_info(request_data,token)
		return Response(response)

class edit_company_info(APIView,Edit_Company_Info_Schema):
	permission_classes=(AllowAny,)
	allowed_methods=("POST",)
	schema=AutoSchema(manual_fields=Edit_Company_Info_Schema().get_manual_fields())
 
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			 "Requested_URL": request.META["PATH_INFO"],
			 
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_edit_company_info(request_data,token)
		return Response(response)

class delete_company(APIView,Delete_Company_Schema):
	permission_classes=(AllowAny,)
	allowed_methods=("POST",)
	schema=AutoSchema(manual_fields=Delete_Company_Schema().get_manual_fields())
 
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			 "Requested_URL": request.META["PATH_INFO"],
			 
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_delete_company(request_data,token)
		return Response(response)

class create_usercompanyrole(APIView,Create_Usercompany_Role_Schema):
	permission_classes=(AllowAny,)
	allowed_methods=("POST",)
	schema=AutoSchema(manual_fields=Create_Usercompany_Role_Schema().get_manual_fields())
 
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			 "Requested_URL": request.META["PATH_INFO"],
			 
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_create_usercompanyrole(request_data,token)
		return Response(response)

class deactivate_usercompanyrole(APIView,Deactivate_Usercompany_Role_Schema):
	permission_classes=(AllowAny,)
	allowed_methods=("POST",)
	schema=AutoSchema(manual_fields=Deactivate_Usercompany_Role_Schema().get_manual_fields())
 
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			 "Requested_URL": request.META["PATH_INFO"],
			 
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_deactivate_usercompanyrole(request_data,token)
		return Response(response)
		
class list_users(APIView,List_Users_Schema):
	permission_classes=(AllowAny,)
	allowed_methods=("POST",)
	schema=AutoSchema(manual_fields=List_Users_Schema().get_manual_fields())
 
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			 "Requested_URL": request.META["PATH_INFO"],
			 
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_list_users(request_data,token)
		return Response(response)
