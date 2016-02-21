from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'pwprice.views.home', name='home'),
    url(r'^api/',include('pwprice.pp_api.urls')),
)
urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)

urlpatterns += staticfiles_urlpatterns()
