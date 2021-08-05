from os import name
import string
import coreapi
import coreschema
from rest_framework import schemas

from rest_framework.schemas import openapi

class Create_Usercompany_Role_Schema(object):
    
    def get_manual_fields(self):
        manual_fields=[
            coreapi.Field(name="Authorization"
                          ,required=True
                          ,location="header"
                          ,schema=coreschema.Object()
                          ,description="Authorization Token of user"
                          ,type="string"
                          ,example="066f3ccce4f344cbad9716b6f8ba9f8a"
                          ),
            coreapi.Field(name="company"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Company id for which role creating"
                          ,type="integer"
                ),
            coreapi.Field(name="user"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="User's id for whome role will created"
                          ,type="integer"
                ),
            coreapi.Field(name="role"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Role id which will assigned"
                          ,type="integer"
                ),
            coreapi.Field(name="flag"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Flag for management"
                          ,type="string"
                          ,example="Company-Management/Project-Management"
                ),
        ]
        return manual_fields