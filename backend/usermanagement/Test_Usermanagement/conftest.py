import pytest
# from usermanagement.utils.store_activity_logs import func_store_activity_logs
from django.conf import settings
from django.utils import timezone
from organization.models import *
from project.models import *
from usermanagement.models import *
from usermanagement.models import AccessManagement, Users
from usermanagement.utils.hash import (decryption, encryption,
                                       generate_passwords)

refresh_lockout = getattr(settings, "LOCKOUT_COUNT_RESET_DURATION", None)
time_threshold = getattr(settings, "INCORRECT_PASSWORD_COUNT_THRESHOLD", None)
count_threshold = getattr(settings, "INCORRECT_PASSWORD_COUNT_MAX_ATTEMPTS", None)
superuser = getattr(settings, "SUPERUSER", None)
superuser_pass = getattr(settings, "SUPERUSERPASS", None)
actvity_logs = getattr(settings, "ACTIVITY_LOGS_DB", None)
error_logs = getattr(settings, "ERROR_LOGS_DB", None)
import logging
import os
import sys
import uuid
from datetime import datetime, timedelta

pytestmark=pytest.mark.django_db


