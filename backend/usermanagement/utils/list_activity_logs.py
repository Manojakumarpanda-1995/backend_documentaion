# from django.conf import settings
import os
import sys
import logging
# from usermanagement.models import AccessManagement, Users
# from usermanagement.utils.hash import decryption, encryption


def func_list_activity_logs(request_data, token):
    try:
        response = {}
        # token = request.META['HTTP_TOKEN']
        try:
            response['message'] = 'Complete'
            response["statuscode"] = 200
            return response
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.info("Error at==>{}".format(e), exc_type, fname, exc_tb.tb_lineno)
            response['message'] = 'Invalid details'
            response["statuscode"] = 400
            return response
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.info("Error at==>{}".format(e), exc_type, fname, exc_tb.tb_lineno)
        response['message'] = 'The username or password is not correct'
        response["statuscode"] = 400
        return response
