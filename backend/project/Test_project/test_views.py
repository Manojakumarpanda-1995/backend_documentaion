import json
import pytest
import random
from faker import Faker 
from usermanagement.models import *
from organization.models import *
from django.conf import settings
from django.urls import reverse
fake = Faker()


class Test_create_project:
    def test(self, client):
        request = reverse("project:create-project")
        data = {}
        response=client.post(request, data=json.dumps(data))
        response = response.json()


class Test_assign_project:
    def test(self, client):
        request = reverse("project:assign-project")
        data = {}
        response = client.post(request, data=json.dumps(data))
        response = response.json()


class Test_list_project:
    def test(self, client):
        request = reverse("project:list-project")
        data = {}
        response = client.post(request, data=json.dumps(data))
        response = response.json()


class Test_list_projects_byemail:
    def test(self, client):
        request = reverse("project:list-project-byemail")
        data = {}
        response = client.post(request, data=json.dumps(data))
        response = response.json()


class Test_edit_project:
    def test(self, client):
        request = reverse("project:edit-project")
        data = {}
        response = client.post(request, data=json.dumps(data))
        response = response.json()


class Test_delete_project:
    def test(self, client):
        request = reverse("project:delete-project")
        data = {}
        response = client.post(request, data=json.dumps(data))
        response = response.json()


class Test_edit_project_user_id:
    def test(self, client):
        request = reverse("project:edit-project-user-id")
        data = {}
        response = client.post(request, data=json.dumps(data))
        response = response.json()


class Test_create_project_user:
    def test(self, client):
        request = reverse("project:create-project-user")
        data = {}
        response = client.post(request, data=json.dumps(data))
        response = response.json()


class Test_list_users_by_project:
    def test(self, client):
        request = reverse("project:list-users-by-project")
        data = {}
        response = client.post(request, data=json.dumps(data))
        response = response.json()

    
class Test_list_projects_for_users:
    def test(self, client): 
        request = reverse("project:list-projects-for-users")
        data = {}
        response = client.post(request, data=json.dumps(data))
        response = response.json()

    
# ## File Upload
class Test_bulk_user_upload:
    def test(self, client):
        request = reverse("project:bulk-user-upload")
        data = {}
        response = client.post(request, data=json.dumps(data))
        response = response.json()


# ## File Download
class Test_bulk_user_download:
    def test(self, client):
        request = reverse("project:bulk-user-download")
        data = {}
        response = client.post(request, data=json.dumps(data))
        response = response.json()


class Test_download:
    def test(self, client):
        request = reverse("project:download-file")
        data = {}
        response = client.post(request, data=json.dumps(data))
        response = response.json()


class Test_download_large_file:
    def test(self, client):
        request = reverse("project:download-large-file")
        data = {}
        response = client.post(request, data=json.dumps(data))
        response = response.json()


# ## Get Progress
class Test_get_progress:
    def test(self, client):
        request = reverse("project:get-progress")
        data = {}
        response = client.post(request, data=json.dumps(data))
        response = response.json()


# # Logs    
class Test_generate_user_logs:
    def test(self, client):
        request = reverse("project:generate-user-logs")
        data = {}
        response = client.post(request, data=json.dumps(data))
        response = response.json()
