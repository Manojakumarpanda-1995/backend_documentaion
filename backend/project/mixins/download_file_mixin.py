import coreapi
import coreschema
import string
from rest_framework import schemas

from rest_framework.schemas import openapi

class Download_File_Schema(object):
    
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
            
            coreapi.Field(name="download_token"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Unique token of file to be downloaded."
                          ,type="integer"
                          ,example="dojk762cd8ae414590ec37f49b66cbf7"
                          ),
        ]
        
        return manual_fields