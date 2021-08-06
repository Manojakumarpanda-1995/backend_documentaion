import coreapi
import string
import coreschema

from rest_framework.schemas import openapi

class Check_Schema(object):
    
    def get_manual_fields(self):
        
        manual_fields=[
            coreapi.Field(name='email'
                            ,required=True
							,location=""
							,schema=coreschema.Object()
                            ,description="Email of user"
                            ,type="string"),
            coreapi.Field(name="Authorization"
                            ,required=True
                            ,location="header"
							,schema=coreschema.Object()
                            ,description="Authorization Token of user"
                            ,type="string"
                            ,example="1a02762cd8ae414590ec37f49b66cbf7"
                            )
            ]
        
        return manual_fields 
        
        
        
        