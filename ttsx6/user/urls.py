from django.conf.urls import url
import views

urlpatterns = [
    url('^islogin/$', views.islogin),
    url('^register/$', views.register),
    url('^register_handle/$', views.register_handle),
    url('^register_valid/$', views.register_valid),
    url('^login/$', views.login),
    url('^logout/$', views.logout),
    url('^login_handle/$', views.login_handle),
    url('^$', views.center),
    url('^order/$', views.order),
    url('^site/$', views.site),

]