import coreapi
import coreschema
import string
from rest_framework import schemas

from rest_framework.schemas import openapi

class List_Projects_Byemail_Schema(object):
    
    def get_manual_fields(self):
        manual_fields=[
            coreapi.Field(name="Authorization"
                          ,required=True
                          ,location="header"
                          ,schema=coreschema.Object()
                          ,description="Authorization Token of User"
                          ,type="string"
                          ,example="1a02762cd8ae414590ec37f49b66cbf7"
                          ),
            coreapi.Field(name="client_id"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Company Id."
                          ,type="integer"
                          ),
            coreapi.Field(name="email"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Email of user whose project to list down."
                          ,type="string"
                          )
        ]
        
        return manual_fields