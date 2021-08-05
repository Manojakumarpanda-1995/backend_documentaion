import coreapi
import string
import coreschema

from rest_framework.schemas import openapi

class Update_Password_Schema(object):
    
    def get_manual_fields(self):
        
        manual_fields=[
            coreapi.Field(name='email'
                            ,required=True
							,location=""
							,schema=coreschema.Object()
                            ,description="Email of user"
                            ,type="string"),
            coreapi.Field(name="new_password"
                            ,required=True
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Password of user"
                            ,type="string"),
            coreapi.Field(name="otp"
                            ,required=True
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Otp send to your email"
                            ,type="string")
            ]
        return manual_fields 
        
        
        
        