"""
URL configuration for infabrica project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic import TemplateView
from django.urls import include, path
from silica.views import message

from infabrica import settings
from infabrica.views import TestView, CPKView, HomeView, LoginView, TestLazyView
from django.contrib import admin


class TestView(TemplateView):
    template_name = "tag_props.html"


urlpatterns = [
    path('tests/tag-props', TestView.as_view()),
    # path("silica/message", message, name="message"),  # to add: /(?P<component_name>[\w/\.-]+)
]

# if settings.DEBUG:
#     urlpatterns += [
#         path("silica-tests/", include("silica.tests.urls")),
#     ]
