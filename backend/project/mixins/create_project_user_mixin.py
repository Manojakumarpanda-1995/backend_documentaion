import coreapi
import coreschema
import string
from rest_framework import schemas

from rest_framework.schemas import openapi

class Create_Project_User_Schema(object):
    
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
            coreapi.Field(name="name"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Name of the Project."
                          ,type="string"
                          ),
            coreapi.Field(name="client_id"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Id of Company."
                          ,type="integer"
                          ),
            coreapi.Field(name="project_id"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Id of project."
                          ,type="integer"
                            ,example="b7e0b7833a9a4fda95545df700c84057"
                          ),
            coreapi.Field(name="user_email"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Email of the User."
                          ,type="string"
                          ),
            coreapi.Field(name="isUser"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="Is this new user."
                          ,type="bollean"
                          ),
            coreapi.Field(name="first_name"
                          ,required=True
                          ,location=""
                          ,schema=coreschema.Object()
                          ,description="First Name of the user."
                          ,type="string"
                          ),
            coreapi.Field(name="lasst_name"
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
        ]
        
        return manual_fields
        
        