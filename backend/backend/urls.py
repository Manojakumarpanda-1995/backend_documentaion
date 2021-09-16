
from re import template

import organization
import project
import usermanagement
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.views.generic.base import TemplateView
from rest_framework.documentation import include_docs_urls
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view
from usermanagement import views

schema_view = get_swagger_view(title='backend API')
                               

# schema_view=get_schema_view(
#     title="backend Api Documents",
#     description="Api documentation for all apis",
#     version='1.0.0',)


urlpatterns = [
    path('doc', schema_view,name='api_documentation'),
    # path('docs/',include_docs_urls(title='api_documentation')),
    # path('loginapi', views.login.as_view(),name="loginapi"),
    # url(r'^$', RedirectView.as_view(url='login')),
    # # url(r'^login$', TemplateView.as_view(template_name='login.html')),
    path("access/",include("usermanagement.urls"),name="usermanagement"),
    path("org/",include("organization.urls"),name="organization"),
    path("project/",include("project.urls"),name="project"),
    path("chat/",include("chatbox.urls"),name="chat"),
    
]#+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
