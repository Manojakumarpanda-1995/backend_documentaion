import os
import mimetypes
import requests
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import FileResponse, StreamingHttpResponse, HttpResponse
from wsgiref.util import FileWrapper
from rest_framework.views import APIView
from rest_framework.response import Response

## Projects
from project.utils.create_project import func_create_project
from project.utils.assign_project import func_assign_project
from project.utils.list_projects import func_list_projects
from project.utils.list_projects_byemail import func_list_projects_byemail
from project.utils.edit_project import func_edit_project
from project.utils.delete_project import func_deactivate_project
from project.utils.edit_project_user_id import func_edit_project_user_id
from project.utils.create_project_user import func_create_project_user
from project.utils.list_users_by_project import func_list_users_by_project
from project.utils.list_project_for_users import func_list_project_for_users
## Get Progress
from project.utils.get_progress import func_get_progress

## Upload File
from project.utils.bulk_upload_users import func_bulk_user_upload
## Download File
from project.utils.bulk_download_users import func_bulk_user_download
from project.utils.download_file import func_download_file
## Logs
from project.utils.generate_user_logs import func_generate_user_logs


# Create your views here.
### Project ##########
# Rohit - Done
class create_project(APIView):
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
class assign_project(APIView):
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
class list_project(APIView):
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
class list_projects_byemail(APIView):
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
class edit_project(APIView):
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
class delete_project(APIView):
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
class edit_project_user_id(APIView):
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

# Rohit - Done
class create_project_user(APIView):
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
		
		
class list_users_by_project(APIView):
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

class list_project_for_users(APIView):
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

### Get Progress ###############
# Rohit - Done
class get_progress(APIView): 
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
		response = func_get_progress(request_data,token)
		return Response(response)


### Upload File ##############
# Rohit - Done
class bulk_upload_users(APIView):
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
class bulk_download_users(APIView):
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
class download_file(APIView):
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
		response = func_download_file(request_data,token)
		# response = FileResponse(open(response["file_path"], "rb"))
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
class generate_user_logs(APIView):
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
