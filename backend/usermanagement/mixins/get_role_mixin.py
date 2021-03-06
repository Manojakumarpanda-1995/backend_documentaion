import coreapi
# import string
import coreschema
# from rest_framework.schemas import openapi


class Get_Role_Schema(object):

    def get_manual_fields(self):

        manual_fields = [
            coreapi.Field(name='Authorization',
                          required=True,
                          location="header",
                          schema=coreschema.Object(),
                          description="User's Authorization token.",
                          type="string",
                          example="1a02762cd8ae414590ec37f49b66cbf7"),
            coreapi.Field(name="role_name",
                          required=True,
                          location="",
                          schema=coreschema.Object(),
                          description="Role Name.",
                          type="string"),
            coreapi.Field(name="company_id",
                          required=False,
                          location="",
                          schema=coreschema.Object(),
                          description="ID of the company.",
                          type="integer"),

            ]

        return manual_fields
