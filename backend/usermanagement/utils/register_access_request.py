import datetime
import logging
import os
import re
import sys
import uuid

from django.conf import settings
# from django.utils import timezone
from organization.models import Company
from usermanagement.models import AccessRequest, Users
from usermanagement.tasks import send_email
# from usermanagement.utils.hash import (decryption, encryption,
#                                        generate_passwords,
#                                        random_alphaNumeric_string)

verify_link_exp = getattr(settings, "VERIFICATION_LINK_EXPIRY_DURATION", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)


# To validate email in the format of foo./_/+/123@some.com
# 0->invalid,1->valid
def validate_email(email):
    try:
        if (re.search("[!#$%^&*()?=,<>/]", email)):
            return 0
        else:
            regex = '[A-Z0-9a-z._+-]+[@][a-z]+[.]+[a-z]{2,3}'
            match = re.match(regex, email)
            # match = re.findall(regex,email)
            return 1 if match else 0
    except Exception as e:
        logging.info("Email_validation==>{}".format(e))


def generate_hash():
    return uuid.uuid4().hex


def func_register_access_request(request_data):
    try:
        response = {}

        logs = {
            "Client_IP_Address": request_data["Client_IP_Address"],
            "Remote_ADDR": request_data["Remote_ADDR"],
            "data": {
                "Requested_URL": request_data["Requested_URL"]
            }
        }
        # To check for the duplicate user
        getUsers = Users.objects.filter(email__iexact=request_data["email"])
        if len(getUsers) != 0:
            logs["data"]["status_message"] = "Users with this email id's already exists. Try an another email."
            response['message'] = "Users with this email id's already exists. Try an another email."

            logs["added_at"] = datetime.datetime.utcnow()
            actvity_logs.insert_one(logs)
            response["statuscode"] = 400
            return response

        # Get all roles
        isAuthorized = True

        apiParamsInfo = {}
        for key, value in request_data.items():
            if key not in ["Client_IP_Address", "Remote_ADDR", "Requested_URL", "company"]:
                apiParamsInfo[key] = value

        # To check for the duplicate company
        getCompanyId = None
        spcl_company_name = re.sub(r'[^A-Za-z0-9\s]+', '', apiParamsInfo["company_name"])
        getCompany = Company.objects.all().values("name", "id")

        for comp in getCompany:
            spcl_comp_name = re.sub(r'[^A-Za-z0-9\s]+', '', comp["name"])

            if spcl_company_name.upper() == spcl_comp_name.upper():
                getCompanyId = comp["id"]
                break

        getCompany = Company.objects.filter(name__iexact=apiParamsInfo["company_name"])
        if getCompanyId is not None or len(getCompany):
            logs["data"]["status_message"] = "Company with this name already registered. To claim contact with admin."
            response['message'] = "Company with this name already registered. To claim contact with admin."

            logs["added_at"] = datetime.datetime.utcnow()
            actvity_logs.insert_one(logs)
            response["statuscode"] = 400
            return response

        if isAuthorized:
            apiParamsInfo["email"] = apiParamsInfo["email"].lower()
            getValidated = validate_email(email=apiParamsInfo['email'])
            if getValidated == 0:
                logs["data"]["status_message"] = "Please try to add valid email."
                response['message'] = "Please try to add valid email."
                response["statuscode"] = 400
                actvity_logs.insert_one(logs)
                return response

            # To validate that name should not blank
            getName = 0 if request_data.get("company_name", None) is None else 1
            getCompany = Company.objects.filter(name__iexact=apiParamsInfo["company_name"])
            getAccess = AccessRequest.objects.filter(email__iexact=apiParamsInfo["email"])

            if getName != 0 and len(getAccess) == 0:
                getAccess = AccessRequest.objects.create(**apiParamsInfo)

                emails = ["rohit@viewooletters.in",
                          "nitin@viewooletters.in"]
                # emails = ["manojakumarpanda@momenttext.com"]
                emails.append(str(getAccess.email))
                message = ("You'r request for Company registration with Company-Name:{} and Email:{} accepted successfully.\n Our Team will contact you soon.".format(
                                                    apiParamsInfo['name'], getAccess.email))

                # # Celery
                # send_email.delay(str({"email": emails,
                #                       "subject": "New Company Registration",
                #                       # "template_name": "generate_passwords",
                #                       "template_name": message,
                #                       # "variables": [decryption(apiParamsInfo['password'])],
                #                       "variables": ['password'],
                #                       # "variables": [decryption(apiParamsInfo['password'])],
                #                       "email_type": "plain"
                #                       }))

                # logging.info("emails==>{}".format(emails))
                logs["data"]["data_fields"] = [apiParamsInfo["company_name"], apiParamsInfo["email"]]
                logs["data"]["status_message"] = "Access requests registered successfully."
                response["data"] = getAccess.id
                response['message'] = 'Access requests registered successfully.'
                response["statuscode"] = 200

            else:
                if len(getAccess) == 0:
                    logs["data"]["status_message"] = "Access requests name can't be left blank."
                    response['message'] = "Access requests name can't be left blank."
                else:
                    logs["data"]["status_message"] = "Access requests with this email already registered."
                    response['message'] = "Access requests with this email already registered."
                logs["data"]["data_fields"] = [apiParamsInfo["email"]]
                response["statuscode"] = 400
        else:
            logs["data"]["data_fields"] = [apiParamsInfo["email"]]
            logs["data"]["status_message"] = 'You are not authorized to create Access requests.'
            response['message'] = 'You are not authorized to create Access requests.'
            response["statuscode"] = 400

        logs["added_at"] = datetime.datetime.utcnow()
        actvity_logs.insert_one(logs)
        return response

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.info(str(exc_type) + " " + str(fname) + " " + str(exc_tb.tb_lineno) + " " + str(e))
        error_logs.insert_one({
            "error_type": str(exc_type),
            "file_name": str(fname),
            "line_no": str(exc_tb.tb_lineno),
            "error": str(e)
        })
        response["statuscode"] = 500
        return response
