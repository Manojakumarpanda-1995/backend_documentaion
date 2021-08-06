import coreapi
import string
import coreschema

from rest_framework.schemas import openapi

class Download_File_Schema(object):
    
    def get_manual_fields(self):
        
        manual_fields=[
            coreapi.Field(name='Authorization'
                            ,required=True
							,location="headers"
							,schema=coreschema.Object()
                            ,description="User's Authorization token."
                            ,type="string"
                            ,example="1a02762cd8ae414590ec37f49b66cbf7"),
            coreapi.Field(name="uid"
                            ,required=True
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Download files token."
                            ,type="string"),
            
            ]
        
        return manual_fields 
        
        
        
        