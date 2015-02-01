from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    
     url(r'^$', 'translations.views.home_page', name='home'),
     url(r'^tms/', include('translations.urls')),
)
