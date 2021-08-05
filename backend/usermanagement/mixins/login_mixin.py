import coreapi
import string
import coreschema

from rest_framework.schemas import openapi

class Login_Schema(object):
    
    def get_manual_fields(self):
        
        manual_fields=[
            coreapi.Field(
                            name='email'
                            ,required=True
							,location=""
							,schema=coreschema.Object()
                            ,description="Email of user"
                            ,type="string"),
            coreapi.Field(name="password"
                            ,required=True
                            ,location=""
							,schema=coreschema.Object()
                            ,description="Password of user"
                            ,type="string")
            ]
        # print("manual_fields=",Login_Schema().get_manual_fields())
	#   manual_fields=[coreapi.Field(#"email"
    #                         name='email'
    #                         ,required=True
    #                         ,location="formdata"#/'query/path/body/location/headers'
    #                           """headers->to pass the headers parameters in request"""
    #                         ,description="Email of user"
    #                         ,type=string),
    #         coreapi.Field(name="password"
    #                         ,required=True
    #                         ,location="formdata"
    #                         ,description="Password of user"
    #                         ,type=string)]	
        return manual_fields 
        
        
        
        