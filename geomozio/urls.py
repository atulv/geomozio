from django.conf.urls import include, url
from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'geomozio.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^apis/', include('apis.urls')),
    url('', views.home),
]
