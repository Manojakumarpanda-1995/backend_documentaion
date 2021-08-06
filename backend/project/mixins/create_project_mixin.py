import coreapi
import coreschema
import string
from rest_framework import schemas

from rest_framework.schemas import openapi

class Create_Project_Schema(object):
    
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
            coreapi.Field(name="name"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Name of the Project."
                          ,type="string"
                          ),
            coreapi.Field(name="description"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Description about the Project."
                          ,type="string"
                          ),
            coreapi.Field(name="client_id"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Id of Company."
                          ,type="integer"
                          )
        ]
        
        return manual_fields