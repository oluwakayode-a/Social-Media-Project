"""earthruh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from . import settings
from sitemaps import PostSitemap
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView


sitemaps = {
    'sitemaps' : PostSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('main.urls', 'main'))),
    path('auth/', include('allauth.urls')),
    path('', include(('accounts.urls', 'accounts'))),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap'),
    path("robots.txt", TemplateView.as_view(template_name="main/robots.txt", content_type="text/plain")),  #add the robots.txt file
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)