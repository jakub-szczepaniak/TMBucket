from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'translations.views.home_page', name='home'),
     url(r'^tms/(\d+)$', 'translations.views.view_tm', name='view_tm'),
     url(r'^tms/(\d+)/add_tunit$', 'translations.views.add_tunit', name='add_tunit'),
     url(r'^tms/new$', 'translations.views.new_tm', name='new_tm'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),

)
