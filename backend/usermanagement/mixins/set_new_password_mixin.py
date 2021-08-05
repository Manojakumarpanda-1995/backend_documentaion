import coreapi
import string
import coreschema

from rest_framework.schemas import openapi

class SetNew_Password_Schema(object):
    
    def get_manual_fields(self):
        
        manual_fields=[
            coreapi.Field(name='Authorization'
                            ,required=True
							,location="headers"
							,schema=coreschema.Object()
                            ,description="Email of user."
                            ,type="string"),
            coreapi.Field(name='email'
                            ,required=True
							,location=""
							,schema=coreschema.Object()
                            ,description="Email of user."
                            ,type="string"),
            coreapi.Field(name="new_password"
                            ,required=True
                            ,location=""
							,schema=coreschema.Object()
                            ,description="New Password to update."
                            ,type="string"),
            coreapi.Field(name="old_password"
                            ,required=True
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Old Password."
                            ,type="string")
            ]
        return manual_fields 
        
        
        
        