import coreapi
import coreschema
import string
from rest_framework import schemas

from rest_framework.schemas import openapi

class Bulk_Upload_Users_Schema(object):
    
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
            coreapi.Field(name="file"
                          ,required=True
                          ,location="formData"
                          ,schema=coreschema.Object()
                          ,description="File to Upload."
                          ,type="file"
                          ),
            coreapi.Field(name="project_id"
                          ,required=True
                          ,location="formData"
                          ,schema=coreschema.Object()
                          ,description="Project's Id for which fie will uploaded."
                          ,type="integer"
                          ),
        ]
        
        return manual_fields