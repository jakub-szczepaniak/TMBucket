from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    
     url(r'^(\d+)/$', 'translations.views.view_tms', name='view_tms'),
     url(r'^(\d+)/add_transunit$', 'translations.views.add_transunit', name='add_transunit'),
     url(r'^new$', 'translations.views.new_tm', name='new_tm'),
    

)
