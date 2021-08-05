import coreapi
import string
import coreschema

from rest_framework.schemas import openapi

class Deactivate_User_Schema(object):
    
    def get_manual_fields(self):
        
        manual_fields=[
            coreapi.Field(name='Authorization'
                            ,required=True
							,location="headers"
							,schema=coreschema.Object()
                            ,description="User's Authorization token."
                            ,type="string"),
            coreapi.Field(name="user_id"
                            ,required=True
                            ,location=""
							,schema=coreschema.Object()
                            ,description="User's ID which will delete."
                            ,type="integer"),
            
            
            ]
	
        
        return manual_fields 
        
        
        
        