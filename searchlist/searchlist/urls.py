"""
URL configuration for searchlist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path
from searchlistapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.homepage, name="homepage"),
    path("ajax_search/", views.ajax_search, name="ajax_search"),
    path("download_excel/", views.download_excel, name="download_excel"),
    path("download-excel/", views.download_excel_writer, name="download_excel_writer"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
