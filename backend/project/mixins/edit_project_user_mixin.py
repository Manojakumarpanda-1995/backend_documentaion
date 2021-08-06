import coreapi
import coreschema
import string
from rest_framework import schemas

from rest_framework.schemas import openapi

class Edit_Project_User_Schema(object):
    
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
            coreapi.Field(name="project_user_id"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Id of project user to be editated."
                          ,type="integer"
                          ),
            coreapi.Field(name="user_email"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Email of the user to update."
                          ,type="string"
                          ),
            coreapi.Field(name="user_first_name"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="First Name of the user."
                          ,type="string"
                          ),
            coreapi.Field(name="user_lasst_name"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Last Name of the user."
                          ,type="string"
                          ),
            coreapi.Field(name="user_role"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Roles to assign to the User."
                          ,type="integer"
                          ),
            coreapi.Field(name="user_expiry_date"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Is this new user."
                          ,type="datetime"
                          ,example="y-m-d H:M"
                          ),
            coreapi.Field(name="user_status"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Status of Projectuser."
                          ,type="boolean"
                          ),
            # coreapi.Field(name="name"
            #               ,required=False
            #               ,location=""
            #               ,schema=coreschema.Object()
            #               ,description="Name of the User."
            #               ,type="string"
            #               ),
            
        ]
        
        return manual_fields
        
        