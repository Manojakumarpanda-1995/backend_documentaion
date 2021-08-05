from os import name
import string
import coreapi
import coreschema
from rest_framework import schemas

from rest_framework.schemas import openapi

class List_Company_Schema(object):
    
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
            coreapi.Field(name="company_id"
                          ,required=False
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Company Id"
                          ,type="integer"
                
            )
            
        ]
        return manual_fields