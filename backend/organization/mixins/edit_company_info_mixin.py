from os import name
import string
import coreapi
import coreschema
from rest_framework import schemas

from rest_framework.schemas import openapi

class Edit_Company_Info_Schema(object):
    
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
            coreapi.Field(name="client_id"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Company Id"
                          ,type="integer"
                ),
            coreapi.Field(name="logo"
                          ,required=False
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Company Logo"
                          ,type="image"
                        #   ,type="file"
                ),
            coreapi.Field(name="corporate_type"
                          ,required=False
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Corporate type of company "
                          ,type="string"
                ),
            coreapi.Field(name="number_of_emploies" 
                          ,required=False
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Number of emploies in the company "
                          ,type="string"
                ),
            coreapi.Field(name="type" 
                          ,required=False
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Type of the company "
                          ,type="string"
                ),
            coreapi.Field(name="links" 
                          ,required=False
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Links of the company "
                          ,type="string"
                ),
            coreapi.Field(name="about" 
                          ,required=False
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="More Info about the company"
                          ,type="string"
                ),
            
        ]
        return manual_fields
    