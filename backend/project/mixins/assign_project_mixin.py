import coreapi
import coreschema
import string
from rest_framework import schemas

from rest_framework.schemas import openapi

class Assign_Project_Schema(object):
    
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
            coreapi.Field(name="user"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="User's Id to which Project will assigned."
                          ,type="integer"
                          ),
            coreapi.Field(name="project"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Project's Id to which user will assigned."
                          ,type="integer"
                          ),
            coreapi.Field(name="client_id"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Companies Id to which Project belong to."
                          ,type="integer"
                          )
        ]
        
        return manual_fields