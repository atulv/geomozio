from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^provider/$', views.provider),
    url(r'^provider/(?P<provider_id>\d+)/update/$', views.update_provider),
    url(r'^provider/(?P<provider_id>\d+)/delete/$', views.remove_provider),
    url(r'^provider/(?P<provider_id>\d+)/service-area/$', views.service_area),
    url(r'^service-area/(?P<service_area_id>\d+)/update/$', views.update_service_area),
    url(r'^service-area/(?P<service_area_id>\d+)/delete/$', views.remove_service_area),
    url(r'^get-service-areas/$', views.query_service_area)
]
