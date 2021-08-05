from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView
from rest_framework.response import Response

## Roles
from organization.utils.list_company import func_list_company
from organization.utils.list_company_byemail import func_list_company_byemail
from organization.utils.create_company import func_create_company
from organization.utils.get_company import func_get_company
from organization.utils.edit_company import func_edit_company
from organization.utils.delete_company import func_delete_company
from organization.utils.create_usercompanyrole import func_create_usercompanyrole
from organization.utils.deactivate_usercompanyrole import func_deactivate_usercompanyrole
from organization.utils.list_users import func_list_users


# Create your views here.

### Company ##########
class list_company(APIView):
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			#"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_list_company(request_data,token)
		return Response(response)


class list_company_byemail(APIView):
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			#"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_list_company_byemail(request_data,token)
		return Response(response)


class create_company(APIView):
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			#"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_create_company(request_data,token)
		return Response(response)


class get_company(APIView):
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			#"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_get_company(request_data,token)
		return Response(response)


class edit_company(APIView):
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			#"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_edit_company(request_data,token)
		return Response(response)


class delete_company(APIView):
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			#"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_delete_company(request_data,token)
		return Response(response)


class create_usercompanyrole(APIView):
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			#"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_create_usercompanyrole(request_data,token)
		return Response(response)

class deactivate_usercompanyrole(APIView):
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			#"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_deactivate_usercompanyrole(request_data,token)
		return Response(response)
		
class list_users(APIView):
	def post(self, request):
		request_data = request.data
		newInfo = {
			"Client_IP_Address": 'localhost' if 'HTTP_X_FORWARDED_FOR' not in request.META else request.META['HTTP_X_FORWARDED_FOR'],
			
			#"Requested_URL": request.META["REQUEST_URI"],
				"Requested_URL": request.META["PATH_INFO"],
			"Remote_ADDR": request.META["REMOTE_ADDR"]
		}
		request_data = {**request_data, **newInfo}
		token = request.META["HTTP_AUTHORIZATION"]
		response = func_list_users(request_data,token)
		return Response(response)