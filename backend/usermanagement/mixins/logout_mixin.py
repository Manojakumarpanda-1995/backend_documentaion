import coreapi
# import string
import coreschema
# from rest_framework.schemas import openapi


class Logout_Schema(object):

    def get_manual_fields(self):

        manual_fields = [
            coreapi.Field(name='email',
                          required=True,
                          location="",
                          schema=coreschema.Object(),
                          description="Email of user",
                          type="string"),
            # coreapi.Field(name="password"
            #                 ,required=True
            #                 ,location=""
            #                 ,schema=coreschema.Object()
            #                 ,description="Password of user"
            #                 ,type="string")
            ]

        return manual_fields
