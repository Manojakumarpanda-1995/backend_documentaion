import logging
from django.http import JsonResponse
import json
from urllib.parse import parse_qs
from usermanagement.models import Users


class CheckToken:
	def __init__(self, get_response):
		self.get_response = get_response
		# One-time configuration and initialization.

	def __call__(self, request):
		try:
			# logging.info(request.META)
			print("request_meta==",request.META)
			# if request.META["REQUEST_URI"].strip("/").split("/")[-1] not in ["loginapi"
			# 			,"register-user"
			# 			,"reset-password","logout"
			# 			,"update-password"] and request.META["REQUEST_METHOD"] == "POST":
			
			if request.META["PATH_INFO"].strip("/").split("/")[-1] not in ["loginapi"
						,"register-user"
						,"reset-password","logout"
						,"update-password"] and request.META["REQUEST_METHOD"] == "POST":
			
				# logging.info(request.META.get("HTTP_AUTHORIZATION",0))
				# logging.info(request.META.get("HTTP_AUTHORIZATION",0))
				request_data = {"token":request.META.get("HTTP_AUTHORIZATION",0)}
				if request_data.get("token",0) == 0:
					logging.info("~1~")
					# logging.info(str(request_data).split("WebKitFormBoundary")[-1])
					return JsonResponse({"statuscode":403})
				else:
					try:
						curr_user = Users.objects.filter(token=request_data["token"])[0]
						if curr_user.user_verified is None or curr_user.user_verified == 0 or curr_user.active == 0:
							return JsonResponse({"statuscode":403})
						else:
							"""
							Only in this case the response will pass this middleware
							"""
							pass
					except Exception as e:#Token did not match
						logging.info("ERROR1->"+str(e))
						return JsonResponse({"statuscode":403})   
			#Checks if the user is verified for Login API
			# elif request.META["REQUEST_URI"].strip("/") == "loginapi" and request.META["REQUEST_METHOD"] == "POST":
			elif request.META["PATH_INFO"].strip("/") == "loginapi" and request.META["REQUEST_METHOD"] == "POST":
				if "application/x-www-form-urlencoded" in request.META["CONTENT_TYPE"]:
					# logging.info("Login API")
					# logging.info(getattr(request, '_body', request.body))
					request_data = parse_qs(getattr(request, '_body', request.body).decode("utf-8"))
					# logging.info(str(request_data))
				elif "application/json" in request.META["CONTENT_TYPE"]:
					# logging.info(getattr(request, '_body', request.body).decode("utf-8") )
					request_data = json.loads(getattr(request, '_body', request.body))
				else:
					# logging.info("LoginAPI content type error")     
					pass
				try:
					# logging.info(request_data["email"])
					curr_user = Users.objects.filter(email=request_data["email"][0])[0]
					# logging.info(curr_user.user_verified)
					if curr_user.user_verified is None or curr_user.user_verified == 0 or curr_user.active == 0:
						return JsonResponse({"statuscode":400,"message":"Your account is not active. Please click on the link sent to your email at the time of Registration."})
					else:
						"""
						Only in this case the response will pass this middleware
						"""
						pass
				except Exception as e:#Email ID did not exist in record
					logging.info("Email does not exists "+str(e))
					return JsonResponse({"statuscode":403})   
			#Only verfied users will be able to use download file APIs.
			#This middleware only checks getfile GET API request, all other GET APIs are passed
			elif (request.META["PATH_INFO"].strip("/") == "download-file" and request.META["REQUEST_METHOD"] == "GET"):      
			# elif (request.META["REQUEST_URI"].strip("/") == "download-file" and request.META["REQUEST_METHOD"] == "GET"):      
				try:
					token = request.META["HTTP_AUTHORIZATION"]
					curr_user = Users.objects.filter(token=token)[0]
					if curr_user.user_verified is None or curr_user.user_verified == 0 or curr_user.active == 0:
						return JsonResponse({"statuscode":403})
					else:
						"""
						Only in this case the response will pass this middleware
						"""
						pass
				except:#Token did not match
					return JsonResponse({"statuscode":403})					
		except Exception as e:
			logging.info("###2####")
			logging.info(e)
			return JsonResponse({"statuscode":403})
		response = self.get_response(request)
		return response        