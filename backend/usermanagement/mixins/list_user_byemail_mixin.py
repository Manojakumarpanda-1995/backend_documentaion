import coreapi
import string
import coreschema

from rest_framework.schemas import openapi

class List_User_Byemail_Schema(object):
    
    def get_manual_fields(self):
        
        manual_fields=[
            coreapi.Field(name='Authorization'
                            ,required=True
							,location="header"
							,schema=coreschema.Object()
                            ,description="User's Authorization token."
                            ,type="string"
                            ,example="1a02762cd8ae414590ec37f49b66cbf7"),
            coreapi.Field(name="email" 
                            ,required=True
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Email of the User."
                            ,type="string"),
            coreapi.Field(name="user_id" 
                            ,required=False
							,location=""
							,schema=coreschema.Object()
                            ,description="User's id."
                            ,type="integer"),
            coreapi.Field(name="company_id"
                            ,required=False
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Company id of user."
                            ,type="integer"),
            ]
	
        
        return manual_fields 
        
        
        
        