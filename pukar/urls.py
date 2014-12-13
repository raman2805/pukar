from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^sos_action/', include('sos_action.urls')),
                       url(r'^admin/', include(admin.site.urls))
    # Examples:
    # url(r'^$', 'pukar.views.home', name='home'),
    # url(r'^pukar/', include('pukar.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
