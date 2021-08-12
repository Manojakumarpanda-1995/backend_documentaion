import coreapi
import coreschema
import string
from rest_framework import schemas

from rest_framework.schemas import openapi

class Generate_Logs_Schema(object):
    
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
                          ,type="integer"
                          
                          ),
            coreapi.Field(name="start_date"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Logs from"
                          ,type="dateTime"
                          
                          ),
            
            coreapi.Field(name="end_date"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Logs to"
                          ,type="dateTime"
                         
                          ),
        ]
        
        return manual_fields