import coreapi
import string
import coreschema

from rest_framework.schemas import openapi

class Create_Role_Schema(object):
    
    def get_manual_fields(self):
        
        manual_fields=[
            coreapi.Field(name='Authorization'
                            ,required=True
							,location="headers"
							,schema=coreschema.Object()
                            ,description="User's Authorization token."
                            ,type="string"),
            coreapi.Field(name="role_name"
                            ,required=True
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Role Name to be created."
                            ,type="string"),
            coreapi.Field(name="role_description"
                            ,required=False
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Description about the role."
                            ,type="string"),
            
            ]
        
        return manual_fields 
        
        
        
        