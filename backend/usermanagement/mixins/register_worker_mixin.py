import coreapi
# import string
import coreschema
# from rest_framework.schemas import openapi


class Register_Worker_Schema(object):

    def get_manual_fields(self):

        manual_fields = [
            coreapi.Field(name='name',
                          required=True,
                          location="",
                          schema=coreschema.Object(),
                          description="Name of user",
                          type="string"),
            coreapi.Field(name='email',
                          required=True,
                          location="",
                          schema=coreschema.Object(),
                          description="Email of user",
                          type="string"),
            coreapi.Field(name='skill_sets',
                          required=True,
                          location="",
                          schema=coreschema.Object(),
                          description="Skills user have",
                          type="string"),
            coreapi.Field(name="phone_no",
                          required=True,
                          location="",
                          schema=coreschema.Object(),
                          description="Ph.No. of user",
                          type="string")
            ]
        return manual_fields
