import pytest
from django.urls import resolve,reverse

class Test_urls:
    
    def test_login_url(self,*args, **kwargs):
        request=reverse("loginapi")
        response=resolve(request)
        print(response)