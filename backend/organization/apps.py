from django.apps import AppConfig


class OrganizationConfig(AppConfig):
	name = 'organization'

	def ready(self):
		try:
			from usermanagement.models import Roles, Users
			from .models import Company, UserCompanyRole

			import re

			# Create Admin Company
			companies = [
				{
					"name": "Administrator",
					"created_by": 1,
					"updated_by": 1,
				}
			]

			for company in companies:
				getCompanyId = None
				spcl_company_name = re.sub('[^A-Za-z0-9\s]+', '', company["name"])
				getCompany = Company.objects.all().values("name", "id")
				
				for comp in getCompany:
					spcl_comp_name = re.sub('[^A-Za-z0-9\s]+', '', comp["name"])

					if spcl_company_name.upper() == spcl_comp_name.upper():
						getCompanyId = comp["id"]
						break
				
				if getCompanyId is None:
					company["created_by"] = Users.objects.filter(id=company["created_by"])[0]
					company["updated_by"] = Users.objects.filter(id=company["updated_by"])[0]

					getCompany = Company.objects.create(**company)



			# Create User Company Role
			userCompanyRole = [
				{
					"user": 1,
					"company": 1,
					"role": 1,
					"created_by": 1,
					"updated_by": 1,
				}
			]

			for companyRole in userCompanyRole:
				getUserCompanyRole = UserCompanyRole.objects.filter(user__id=companyRole["user"],
																	company__id=companyRole["company"],
																	role__id=companyRole["role"])
				
				if len(getUserCompanyRole) == 0:
					companyRole["created_by"] = Users.objects.filter(id=companyRole["created_by"])[0]
					companyRole["updated_by"] = Users.objects.filter(id=companyRole["updated_by"])[0]
					companyRole["user"] = Users.objects.filter(id=companyRole["user"])[0]
					companyRole["company"] = Company.objects.filter(id=companyRole["company"])[0]
					companyRole["role"] = Roles.objects.filter(id=companyRole["role"])[0]

					getUserCompanyRole = UserCompanyRole.objects.create(**companyRole)
		except:
			pass