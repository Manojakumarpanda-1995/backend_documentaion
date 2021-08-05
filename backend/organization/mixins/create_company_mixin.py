from os import name
import string
import coreapi
import coreschema
from rest_framework import schemas

from rest_framework.schemas import openapi

class Create_Company_Schema(object):
    
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
            coreapi.Field(name="name"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Name of Company"
                          ,type="string"
                ),    
            coreapi.Field(name="address1"
                          ,required=False
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Address1 of Company"
                          ,type="string"
                ),
            coreapi.Field(name="address2"
                          ,required=False
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Address2 of Company"
                          ,type="string"
                ),
            coreapi.Field(name="city"
                          ,required=False
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="City Name"
                          ,type="string"
                ),
            coreapi.Field(name="state"
                          ,required=False
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="State Name"
                          ,type="integer"
                ),
            coreapi.Field(name="country"
                          ,required=False
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Country Name"
                          ,type="string"
                ),
            coreapi.Field(name="partner_name"
                          ,required=False
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Partner Name"
                          ,type="string"
                ),
            coreapi.Field(name="state_pin_code"
                          ,required=False
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="State Pin Code"
                          ,type="integer"
                )
            
        ]
        return manual_fields

	
	