import logging
from coreschema.schemas import Schema

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView

#importing the mixins for schemas
from usermanagement.mixins.check_token_mixin import Check_Schema
from usermanagement.mixins.create_role_mixin import Create_Role_Schema
from usermanagement.mixins.deactivate_user_mixin import \
    Deactivate_User_Schema
from usermanagement.mixins.download_file_mixin import Download_File_Schema
from usermanagement.mixins.edit_user_byid_mixin import \
    Edit_User_byid_Schema
from usermanagement.mixins.edit_user_mixin import Edit_User_Schema
from usermanagement.mixins.get_role_mixin import Get_Role_Schema
from usermanagement.mixins.list_user_byemail_mixin import \
    List_User_Byemail_Schema
from usermanagement.mixins.login_mixin import Login_Schema
from usermanagement.mixins.logout_mixin import Logout_Schema
from usermanagement.mixins.register_access_mixin import Register_Access_Schema
from usermanagement.mixins.register_user_mixin import Register_User_Schema
from usermanagement.mixins.register_worker_mixin import Register_Worker_Schema
from usermanagement.mixins.reset_password_request_mixin import \
    Reset_Password_Request_Schema
from usermanagement.mixins.set_new_password_mixin import SetNew_Password_Schema
from usermanagement.mixins.update_password_mixin import Update_Password_Schema

from usermanagement.utils.check_token import func_check_token
from usermanagement.utils.create_role import func_create_role
from usermanagement.utils.delete_user import func_delete_user
from usermanagement.utils.download_file import func_download_file
from usermanagement.utils.edit_user import func_edit_user
from usermanagement.utils.edit_user_byid import func_edit_user_byid
from usermanagement.utils.get_role import func_get_role
from usermanagement.utils.list_user_byemail import func_list_user_byemail
from usermanagement.utils.login import func_login
from usermanagement.utils.logout import func_logout
from usermanagement.utils.register_access_request import \
    func_register_access_request
from usermanagement.utils.register_user import func_register_user
from usermanagement.utils.register_worker import func_register_worker
from usermanagement.utils.reset_password_request import \
    func_reset_password_request
from usermanagement.utils.set_new_password import func_set_new_password
from usermanagement.utils.update_password import func_update_password

from .serializer import *


class login(APIView,Login_Schema):
	serializer_class =UserSerializer#,many=True)
	permission_classes = (AllowAny,)
	allowed_methods = ('POST',)
	schema=AutoSchema(manual_fields=Login_Schema().get_manual_fields())
    
	def post(self, request,format=None):
		request_data = request.data
		newInfo = {
				"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
				# "Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
				"Remote_ADDR": request.META["REMOTE_ADDR"]
			}
		request_data = {**request_data, **newInfo}
		print("request_data==>",request.data)
		response = func_login(request_data)
		return Response(response)

class reset_password_request(APIView,Reset_Password_Request_Schema):
	permission_classes = (AllowAny,)
	allowed_methods = ('POST',)
	schema=AutoSchema(manual_fields=Reset_Password_Request_Schema().get_manual_fields())
    
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			# "Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		response = func_reset_password_request(request_data)
		return Response(response)

class update_password(APIView,Update_Password_Schema):
	permission_classes = (AllowAny,)
	allowed_methods = ('POST',)
	schema=AutoSchema(manual_fields=Update_Password_Schema().get_manual_fields())
    
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			# "Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		response = func_update_password(request_data)
		return Response(response)

class register_worker(APIView,Register_Worker_Schema):
	permission_classes = (AllowAny,)
	allowed_methods = ('POST',)
	schema=AutoSchema(manual_fields=Register_Worker_Schema().get_manual_fields())
 
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			# "Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		response = func_register_worker(request_data)
		return Response(response)

class register_access_request(APIView,Register_Access_Schema):
	permission_classes = (AllowAny,)
	allowed_methods = ('POST',)
	schema=AutoSchema(manual_fields=Register_Access_Schema().get_manual_fields())
 
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			# "Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		response = func_register_access_request(request_data)
		return Response(response)

class logout(APIView,Logout_Schema):
	permission_classes = (AllowAny,)
	allowed_methods = ('POST',)
	schema=AutoSchema(manual_fields=Logout_Schema().get_manual_fields())
 
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			# "Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		# token = request.META["HTTP_AUTHORIZATION"]
		response = func_logout(request_data)
		return Response(response)
		
class check_token(APIView,Check_Schema):
	permission_classes = (AllowAny,)
	allowed_methods = ('POST',)
	schema=AutoSchema(manual_fields=Check_Schema().get_manual_fields())
 
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			# "Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		# logging.info("request_headers==>{}".format(request.META))
		response = func_check_token(request_data,token)
		return Response(response)

class set_new_password(APIView,SetNew_Password_Schema):
	permission_classes = (AllowAny,)
	allowed_methods = ('POST',)
	schema=AutoSchema(manual_fields=SetNew_Password_Schema().get_manual_fields())
    
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			# "Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_set_new_password(request_data, token)
		return Response(response)

class register_user(APIView,Register_User_Schema):
	permission_classes = (AllowAny,)
	allowed_methods = ('POST',)
	schema=AutoSchema(manual_fields=Register_User_Schema().get_manual_fields())
 
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			# "Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_register_user(request_data, token)
		return Response(response)

class deactivate_user(APIView,Deactivate_User_Schema):
	permission_classes = (AllowAny,)
	allowed_methods = ('POST',)
	schema=AutoSchema(manual_fields=Deactivate_User_Schema().get_manual_fields())
 
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			# "Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_delete_user(request_data, token)
		return Response(response)

class edit_user(APIView,Edit_User_Schema):
	permission_classes=[AllowAny,]
	allowed_methods=("POST",)
	schema=AutoSchema(manual_fields=Edit_User_Schema().get_manual_fields())
    
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			# "Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_edit_user(request_data, token)
		return Response(response)

class edit_user_byid(APIView,Edit_User_byid_Schema):
	permission_classes=[AllowAny,]
	allowed_methods=("POST",)
	schema=AutoSchema(manual_fields=Edit_User_byid_Schema().get_manual_fields())
    
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			# "Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_edit_user_byid(request_data, token)
		return Response(response)

class list_user_byemail(APIView,List_User_Byemail_Schema):
	permission_classes=[AllowAny,]
	allowed_methods=("POST",)
	schema=AutoSchema(manual_fields=List_User_Byemail_Schema().get_manual_fields())
 
	def post(self, request):
		request_data=request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			# "Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_list_user_byemail(request_data, token)
		return Response(response)

### Roles ##########
class create_role(APIView,Create_Role_Schema):
	permission_classes=[AllowAny,]
	allowed_methods=("POST",)
	schema=AutoSchema(manual_fields=Create_Role_Schema().get_manual_fields())
 
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			# "Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_create_role(request_data,token)
		return Response(response)

class get_role(APIView,Get_Role_Schema):
	permission_classes=[AllowAny,]
	allowed_methods=("POST",)
	schema=AutoSchema(manual_fields=Get_Role_Schema().get_manual_fields())
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			# "Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_get_role(request_data,token)
		return Response(response)
		
## Download file get request
class download_file(APIView,Download_File_Schema):
	permission_classes=(AllowAny,)
	schema=AutoSchema(manual_fields=Download_File_Schema().get_manual_fields())
    
	def get(self, request):
		request_data = request.query_params
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			# "Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]		
		response = func_download_file(request_data,token)
		return response			


