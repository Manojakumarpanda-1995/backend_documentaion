import coreapi
import string
import coreschema

from rest_framework.schemas import openapi

class Edit_User_byid_Schema(object):
    
    def get_manual_fields(self):
        
        manual_fields=[
            coreapi.Field(name='Authorization'
                            ,required=True
							,location="headers"
							,schema=coreschema.Object()
                            ,description="User's Authorization token."
                            ,type="string"
                            ,example="1a02762cd8ae414590ec37f49b66cbf7"),
            coreapi.Field(name="user_id" 
                            ,required=True
                            ,location=""
							,schema=coreschema.Object()
                            ,description="User's ID to be edited."
                            ,type="string"),
            coreapi.Field(name="email" 
                            ,required=False
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Email of the User."
                            ,type="string"),
            coreapi.Field(name="first_name" 
                            ,required=False
							,location=""
							,schema=coreschema.Object()
                            ,description="First Name of user."
                            ,type="string"),
            coreapi.Field(name="last_name"
                            ,required=False
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Last Name of user."
                            ,type="string"),
            coreapi.Field(name="name"
                            ,required=True
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Name of the user."
                            ,type="string"),
            coreapi.Field(name="designation"
                            ,required=False
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Designation of the user."
                            ,type="string"),
            coreapi.Field(name="reporting_manager_id"
                            ,required=False
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Reporting manager's ID."
                            ,type="integer"),
            coreapi.Field(name="reporting_manager_name"
                            ,required=False
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Reprting Managers Name."
                            ,type="string"),
            coreapi.Field(name="reporting_manager_email"
                            ,required=False
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Reporting managers email."
                            ,type="string"),
            ]
	
        
        return manual_fields 
        
        
        
        