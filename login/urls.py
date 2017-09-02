from django.conf.urls import include, url
from login import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'FieldManagement.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^/admin', views.admin_login, name = "ALogin" ),
    url(r'^/student', views.student_login, name = "SLogin" ),
    url(r'^/professor', views.professsor_login, name = "PFLogin" ),
    url(r'^/plotManager', views.plotManager_login, name = "PMLogin" ),
    url(r'^/logout', views.Loginlogout, name = "logout" ),
    # url(r'^/plotManager', views.pmanager_login, name = "SLogin" ),
    # url(r'^/student', views.student_login, name = "SLogin" ),
    # url(r'^/professor', views.professor_login, name = "PFLogin" ),
]