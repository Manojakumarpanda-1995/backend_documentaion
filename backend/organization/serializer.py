from rest_framework import serializers
from usermanagement.models import *
from usermanagement.serializer import *
from . models import *
# from

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        models=Company
        fields="__all__"
    
class UserCompanyRoleSerializer(serializers.ModelSerializer):
    
    class Meta:
        models=UserCompanyRole
        fields='__all__'
       

    
    
    