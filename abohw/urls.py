"""abohw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from .sitemaps import StaticViewSitemap
from django.conf.urls import handler404
from django.contrib.sitemaps.views import sitemap
from web.views import webHome
from work.views import workHome
from photos.views import photosHome, photosRandom

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('work-with-me/', workHome, name='work'),
    path('work/', RedirectView.as_view(pattern_name='work', permanent=True)),
    path('photos/', photosHome, name='photos'),
    path('photos/random', photosRandom, name='random-photo'),
    path('photos/<str:page>', photosHome),
    path('', webHome, name='home'),
    path('blog/', RedirectView.as_view(url='https://medium.com/@abohw/', permanent=True)),
    path('blog/<page>', RedirectView.as_view(url='https://medium.com/@abohw/%(page)s', permanent=False)),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'web.views.error404'
