
import mimetypes
import os
from wsgiref.util import FileWrapper

import requests
from django.http import FileResponse, HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework import schemas
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.schemas import AutoSchema

#mixins
from project.mixins.assign_project_mixin import Assign_Project_Schema
from project.mixins.bulk_upload_fies_mixin import Bulk_Upload_Users_Schema
from project.mixins.create_project_mixin import Create_Project_Schema
from project.mixins.create_project_user_mixin import \
    Create_Project_User_Schema 
from project.mixins.delete_project_mixin import Delete_Project_Schema
from project.mixins.download_file_mixin import Download_File_Schema
from project.mixins.bulk_download_user_mixin import \
    Bulk_Download_Users_Schema
from project.mixins.edit_project_mixin import Edit_Project_Schema
from project.mixins.edit_project_user_mixin import \
    Edit_Project_User_Schema
from project.mixins.generate_logs_mixin import Generate_Logs_Schema
from project.mixins.list_project_mixin import List_Projects_Schema
from project.mixins.list_project_byemail_mixin import \
    List_Projects_Byemail_Schema
from project.mixins.list_project_for_users_mixin import \
    List_Project_For_Users_Schema
from project.mixins.list_users_by_project_mixin import \
    List_Users_by_Project_Schema
## Download File
from project.utils.assign_project import func_assign_project
from project.utils.bulk_download_users import func_bulk_user_download
## Upload File
from project.utils.bulk_upload_users import func_bulk_user_upload
## Projects
from project.utils.create_project import func_create_project
from project.utils.create_project_user import func_create_project_user
from project.utils.delete_project import func_deactivate_project
from project.utils.download_file import func_download_file
from project.utils.edit_project import func_edit_project
from project.utils.edit_project_user_id import func_edit_project_user_id
## Logs
from project.utils.generate_user_logs import func_generate_user_logs
## Get Progress
from project.utils.get_progress import func_get_progress
from project.utils.list_project_for_users import func_list_project_for_users
from project.utils.list_projects import func_list_projects
from project.utils.list_projects_byemail import func_list_projects_byemail
from project.utils.list_users_by_project import func_list_users_by_project


# Create your views here.
### Project ##########
# Rohit - Done
class create_project(APIView,Create_Project_Schema):
	allowed_methods=("POST",)
	permission_classes=(AllowAny,)
	schema=AutoSchema(manual_fields=Create_Project_Schema().get_manual_fields())
    
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			# #"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_create_project(request_data,token)
		return Response(response)

# Rohit - Done
class assign_project(APIView,Assign_Project_Schema):
	allowed_methods=("POST",)
	permission_classes=(AllowAny,)
	schema=AutoSchema(manual_fields=Assign_Project_Schema().get_manual_fields())
	
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			# #"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_assign_project(request_data,token)
		return Response(response)

# Rohit - Done
class list_project(APIView,List_Projects_Schema):
	allowed_methods=("POST",)
	permission_classes=(AllowAny,)
	schema=AutoSchema(manual_fields=List_Projects_Schema().get_manual_fields())
 
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			# #"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_list_projects(request_data,token)
		return Response(response)

# Rohit - Done
class list_projects_byemail(APIView,List_Projects_Byemail_Schema):
	allowed_methods=("POST",)
	permission_classes=(AllowAny,)
	schema=AutoSchema(manual_fields=List_Projects_Byemail_Schema().get_manual_fields())
 
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			# #"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_list_projects_byemail(request_data,token)
		return Response(response)

# Rohit - Done
class edit_project(APIView,Edit_Project_Schema):
	allowed_methods=("POST",)
	permission_classes=(AllowAny,)
	schema=AutoSchema(manual_fields=Edit_Project_Schema().get_manual_fields())
 
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			# #"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_edit_project(request_data,token)
		return Response(response)

# Rohit - Done
class delete_project(APIView,Delete_Project_Schema):
	allowed_methods=("POST",)
	permission_classes=(AllowAny,)
	schema=AutoSchema(manual_fields=Delete_Project_Schema().get_manual_fields())
 
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			# #"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_deactivate_project(request_data,token)
		return Response(response)

# Rohit - Done
class create_project_user(APIView,Create_Project_User_Schema):
	allowed_methods=("POST",)
	permission_classes=(AllowAny,)
	schema=AutoSchema(manual_fields=Create_Project_User_Schema().get_manual_fields())
 
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			# #"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_create_project_user(request_data,token)
		return Response(response)

# Rohit - Done
class edit_project_user_id(APIView,Edit_Project_User_Schema):
	allowed_methods=("POST",)
	permission_classes=(AllowAny,)
	schema=AutoSchema(manual_fields=Edit_Project_User_Schema().get_manual_fields())
 
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			# #"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_edit_project_user_id(request_data,token)
		return Response(response)
				
class list_users_by_project(APIView,List_Users_by_Project_Schema):
	allowed_methods=("POST",)
	permission_classes=(AllowAny,)
	schema=AutoSchema(manual_fields=List_Users_by_Project_Schema().get_manual_fields())
 
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			# #"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_list_users_by_project(request_data,token)
		return Response(response)		

class list_project_for_users(APIView,List_Project_For_Users_Schema):  
	allowed_methods=("POST",)
	permission_classes=(AllowAny,)
	schema=AutoSchema(manual_fields=List_Project_For_Users_Schema().get_manual_fields())
 
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			# #"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_list_project_for_users(request_data,token)
		return Response(response)

### Upload File ##############
# Rohit - Done
class bulk_upload_users(APIView,Bulk_Upload_Users_Schema):
	allowed_methods=("POST",)
	permission_classes=(AllowAny,)
	schema=AutoSchema(manual_fields=Bulk_Upload_Users_Schema().get_manual_fields())
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			# #"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_bulk_user_upload(request_data,token)
		return Response(response)

### Download File ##############
# Rohit - Done
class bulk_download_users(APIView,Bulk_Download_Users_Schema):
	allowed_methods=("POST",)
	permission_classes=(AllowAny,)
	schema=AutoSchema(manual_fields=Bulk_Download_Users_Schema().get_manual_fields())
	
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			# #"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_bulk_user_download(request_data,token)
		return Response(response)

# Rohit - Done
class download_file(APIView,Download_File_Schema):
	allowed_methods=("POST",)
	permission_classes=(AllowAny,)
	schema=AutoSchema(manual_fields=Download_File_Schema().get_manual_fields())
 
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			# #"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_download_file(request_data,token)
		return Response(response)

### Get Progress ###############
# Rohit - Done
class get_progress(APIView): 
	def get(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			# #"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		request_data["download_token"] = request.query_params["download_token"]
		token = request.META["HTTP_AUTHORIZATION"]
		# response = FileResponse(open(response["file_path"], "rb"))
		response = func_get_progress(request_data,token)
		return FileResponse(open(response["file_path"], "rb"))

# Rohit - Done
class download_large_file(APIView):
	def get(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			# #"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		request_data["download_token"] = request.query_params["download_token"]
		token = request.META["HTTP_AUTHORIZATION"]
		func_response = func_download_file(request_data,token)
		
		# req = requests.get(func_response["file_path"], stream=True)
		response = FileResponse(FileWrapper(open(func_response["file_path"], "rb")), content_type=mimetypes.guess_type(func_response["file_path"])[0])
		# response = StreamingHttpResponse(open(func_response["file_path"], "rb"), content_type='multipart/x-mixed-replace')
		response['Content-Length'] = os.path.getsize(func_response["file_path"])
		# response['Content-Disposition'] = "attachment; filename={}".format(os.path.basename(func_response["file_path"]))
		# return FileResponse(open(response["file_path"], "rb"))
		
		return response

### Logs ##############
# Rohit - Done
class generate_user_logs(APIView,Generate_Logs_Schema):
	permission_classes=(AllowAny,)
	schema=AutoSchema(manual_fields=Generate_Logs_Schema().get_manual_fields())
    
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			# #"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_generate_user_logs(request_data,token)
		return Response(response)
