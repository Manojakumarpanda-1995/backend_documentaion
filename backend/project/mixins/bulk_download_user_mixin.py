import coreapi
import coreschema
import string
from rest_framework import schemas

from rest_framework.schemas import openapi

class Bulk_Download_Users_Schema(object):
    
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
                          ,description="Project's Id for which user wil be downloaded."
                          ,type="string"
                          ,example="dojk762cd8ae414590ec37f49b66cbf7"
                          ),
        ]
        
        return manual_fields