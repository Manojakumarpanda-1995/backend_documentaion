# from typing_extensions import Required
from rest_framework import serializers
from . models import *
from  organization.models import *
from  organization.serializer import *

# from

class AccessManagementSerializer(serializers.ModelSerializer):

    class Meta:
        models=Users
        fields="__all__"
        
    def create(self, validated_data):
        return Users.objects.get_or_create(**validated_data)

class ActivityLogsSerializer(serializers.ModelSerializer):
    
    class Meta:
        models=ActivityLogs
        fields='__all__'

class TemporaryURLSerializer(serializers.ModelSerializer):
    
    class Meta:
        models=TemporaryURL
        fields='__all__'
       
class UserSerializer(serializers.ModelSerializer):
    accessmanagement=AccessManagementSerializer(many=True,read_only=True)
    activitylogs=ActivityLogsSerializer(many=True,read_only=True)
    temporaryurl=TemporaryURLSerializer(many=True,read_only=True)
    usercompanyrole=UserCompanyRoleSerializer(many=True,read_only=True)
    
    class Meta:
        models=Users
        fields="__all__"
        
    # def create(self, validated_data):
    #     return Users.objects.get_or_create(**validated_data)
    
class RolesSerializer(serializers.ModelSerializer):
    
    class Meta:
        models=Roles
        fields='__all__'
       
class LoginSerializer(serializers.Serializer):
    
    email=serializers.CharField(max_length=100,required=True)
    password=serializers.CharField(max_length=100,required=True)
       

    
    
    