import coreapi
import string
from rest_framework.schemas import AutoSchema, openapi

class Custom_Schema(AutoSchema):
    
	# def __init__(self):

    #     return super(Custom_Schema, self).__init__
    
	def get_manual_fields(self, path, method):

		self.extra_fields=[
			coreapi.Field(name="email"
                            ,required=True
                            ,location="form"
                            # ,schema=openapi.TYPE_STRING
                            # ,schema=coreschema.String(title="name", description="description")
                            ,description="Email of user"
                            ,type=string),
            coreapi.Field(name="password"
                            ,required=True
                            ,location="form"
                            ,description="Password of user"
                            ,type=string)
		]
		manual_fields=super().get_manual_fields(path, method)
		return self.manual_fields+self.extra_fields