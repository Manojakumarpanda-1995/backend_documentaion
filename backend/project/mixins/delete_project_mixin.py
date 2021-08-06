import coreapi
import coreschema
import string
from rest_framework import schemas

from rest_framework.schemas import openapi

class Delete_Project_Schema(object):
    
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
            coreapi.Field(name="project_id"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Project Id to be deleted."
                          ,type="integer"
                          ),
            coreapi.Field(name="status"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Status of the project."
                          ,type="boolean"
                          )
        ]
        
        return manual_fields