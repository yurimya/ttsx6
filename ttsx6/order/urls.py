from django.conf.urls import url
<<<<<<< HEAD

urlpatterns = [

=======
import views
urlpatterns = [
    url('^$', views.do_order),
>>>>>>> itcast
]