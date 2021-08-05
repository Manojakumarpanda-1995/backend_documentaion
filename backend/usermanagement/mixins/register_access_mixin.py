import coreapi
import string
import coreschema

from rest_framework.schemas import openapi

class Register_Access_Schema(object):
    
    def get_manual_fields(self):
        
        manual_fields=[
            coreapi.Field(name="name"
                            ,required=True
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Name of the Company-Amdin."
                            ,type="string"),
            coreapi.Field(name='email'
                            ,required=True
							,location=""
							,schema=coreschema.Object()
                            ,description="Email of Company-Admin"
                            ,type="string"),
            coreapi.Field(name="company_name"
                            ,required=True
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Company Name to be Registered."
                            ,type="string"),
            coreapi.Field(name="phone_number"
                            ,required=True
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Phone Number of Company-Admin."
                            ,type="string"),
            coreapi.Field(name="skill_sets"
                            ,required=True
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Skill set required by company."
                            ,type="string"),
            ]
       
        return manual_fields 
        
        
        
        