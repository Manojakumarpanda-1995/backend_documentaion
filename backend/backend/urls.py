
from re import template
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
import organization,usermanagement,project
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic import RedirectView
from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from usermanagement import views

# schema_view=get_schema_view(
#     title="backend Api Documents",
#     description="Api documentation for all apis",
#     version='1.0.0',)

schema_view = get_swagger_view(title='backend API')

# schema_view=get_schema_view(
    # title="backend Api Documents",
#     description="Api documentation for all apis",
#     version='1.0.0',)


urlpatterns = [
   path('', schema_view,name='api_documentation'),
    path('docs/',include_docs_urls(title='api_documentation')),
    # path('loginapi', views.login.as_view(),name="loginapi"),
    # url(r'^$', RedirectView.as_view(url='login')),
    url(r'^login$', TemplateView.as_view(template_name='login.html')),
    path("access/",include("usermanagement.urls"),name="usermanagement"),
    path("org/",include("organization.urls"),name="organization"),
    path("project/",include("project.urls"),name="project"),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
