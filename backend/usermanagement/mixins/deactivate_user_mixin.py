import coreapi
import string
import coreschema

from rest_framework.schemas import openapi

class Deactivate_User_Schema(object):
    
    def get_manual_fields(self):
        
        manual_fields=[
            coreapi.Field(name='Authorization'
                            ,required=True
							,location="header"
							,schema=coreschema.Object()
                            ,description="User's Authorization token."
                            ,type="string"
                            ,example="1a02762cd8ae414590ec37f49b66cbf7"),
            coreapi.Field(name="user_id"
                            ,required=True
                            ,location=""
							,schema=coreschema.Object()
                            ,description="User's ID which will delete."
                            ,type="integer"),
            coreapi.Field(name="status"
                            ,required=True
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Status of the user."
                            ,type="boolean"),
            
            
            ]
	
        
        return manual_fields 
        
        
        
        